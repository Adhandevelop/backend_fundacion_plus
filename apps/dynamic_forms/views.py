import uuid
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsCitizenOnly
from apps.audit.services import AuditService
from apps.dynamic_forms.models import (
    Formulario,
    FormularioEnvio,
    FormularioVersion,
)
from apps.dynamic_forms.permissions import CanManageForms
from apps.dynamic_forms.serializers import (
    AdminFormularioCreateUpdateSerializer,
    AdminFormularioDetailSerializer,
    AdminFormularioListSerializer,
    AdminFormularioSubmissionDetailSerializer,
    AdminFormularioSubmissionListSerializer,
    CitizenSubmissionDetailSerializer,
    CitizenSubmissionListSerializer,
    FormularioVersionDetailSerializer,
    PublicActivationResendSerializer,
    PublicActivationVerifySerializer,
    PublicFormularioDetailSerializer,
    PublicFormularioSubmitSerializer,
)
from apps.dynamic_forms.services import (
    FormularioExportService,
    FormularioService,
    FormularioSubmissionService,
    FormularioTokenService,
)
from apps.dynamic_forms.validators import validate_idempotency_key


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdminFormularioViewSet(viewsets.ModelViewSet):
    """
    CRUD y ciclo de vida de formularios dinámicos para administradores (can_manage_forms).
    """
    queryset = Formulario.objects.all().prefetch_related('versiones', 'preguntas_borrador')
    permission_classes = [CanManageForms]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminFormularioListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return AdminFormularioCreateUpdateSerializer
        return AdminFormularioDetailSerializer

    def get_object(self):
        lookup = self.kwargs.get(self.lookup_field)
        queryset = self.filter_queryset(self.get_queryset())
        try:
            uuid_val = uuid.UUID(str(lookup))
            return get_object_or_404(queryset, pk=uuid_val)
        except (ValueError, TypeError):
            return get_object_or_404(queryset, slug__iexact=str(lookup))

    def get_queryset(self):
        qs = Formulario.objects.all().prefetch_related('versiones', 'preguntas_borrador')
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(titulo__icontains=search) | Q(slug__icontains=search))
        estado = self.request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        return qs.order_by('-fecha_creacion')

    def perform_create(self, serializer):
        formulario = serializer.save(creado_por=self.request.user)
        AuditService.set_db_actor_session(self.request.user)
        AuditService.log(
            actor=self.request.user,
            action='create',
            module='formularios_dinamicos',
            target_model='formularios',
            target_id=formulario.id,
            description=f'Creación de borrador de formulario "{formulario.titulo}"',
        )

    def perform_update(self, serializer):
        formulario = serializer.instance
        if formulario.estado == Formulario.Estado.ARCHIVADO:
            raise ValidationError('Un formulario archivado es de solo lectura y no puede modificarse.')
        FormularioService.save_draft(formulario, serializer.validated_data, actor=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        formulario = self.get_object()
        version = FormularioService.publish_version(formulario, actor=request.user)
        return Response({
            'mensaje': 'Formulario publicado exitosamente.',
            'estado': formulario.estado,
            'numero_version': version.numero_version,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        formulario = self.get_object()
        FormularioService.close_formulario(formulario, actor=request.user)
        return Response({
            'mensaje': 'Formulario cerrado. Ya no admitirá nuevos envíos públicos.',
            'estado': formulario.estado,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        formulario = self.get_object()
        FormularioService.reopen_formulario(formulario, actor=request.user)
        return Response({
            'mensaje': 'Formulario reabierto exitosamente.',
            'estado': formulario.estado,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        formulario = self.get_object()
        FormularioService.archive_formulario(formulario, actor=request.user)
        return Response({
            'mensaje': 'Formulario archivado históricamente.',
            'estado': formulario.estado,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        formulario = self.get_object()
        nuevo = FormularioService.duplicate_formulario(formulario, actor=request.user)
        serializer = AdminFormularioDetailSerializer(nuevo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path=r'versions/(?P<version_num>[0-9]+)')
    def version_detail(self, request, pk=None, version_num=None):
        """P17: Consulta administrativa detallada de una versión congelada con preguntas y opciones."""
        formulario = self.get_object()
        version = get_object_or_404(
            formulario.versiones.prefetch_related('preguntas__opciones'),
            numero_version=int(version_num),
        )
        serializer = FormularioVersionDetailSerializer(version)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path=r'versions/(?P<version_num>[0-9]+)/create-draft')
    def create_draft(self, request, pk=None, version_num=None):
        formulario = self.get_object()
        FormularioService.create_draft_from_version(formulario, int(version_num), actor=request.user)
        serializer = AdminFormularioDetailSerializer(formulario)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={200: AdminFormularioSubmissionListSerializer(many=True)},
        summary='Listar envíos/respuestas de un formulario con filtros y paginación (ADM, P25)',
    )
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        formulario = self.get_object()
        qs = FormularioEnvio.objects.filter(formulario=formulario).select_related('version', 'usuario')

        version_param = request.query_params.get('version')
        if version_param:
            try:
                qs = qs.filter(version__numero_version=int(version_param))
            except (ValueError, TypeError):
                pass
        estado_v = request.query_params.get('estado_vinculacion')
        if estado_v:
            qs = qs.filter(estado_vinculacion=estado_v)
        fecha_desde = request.query_params.get('fecha_desde')
        if fecha_desde:
            qs = qs.filter(fecha_envio__gte=fecha_desde)
        fecha_hasta = request.query_params.get('fecha_hasta')
        if fecha_hasta:
            qs = qs.filter(fecha_envio__lte=fecha_hasta)

        ordered_qs = qs.order_by('-fecha_envio')
        page = self.paginate_queryset(ordered_qs)
        if page is not None:
            serializer = AdminFormularioSubmissionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AdminFormularioSubmissionListSerializer(ordered_qs, many=True)
        return Response({
            'count': len(serializer.data),
            'next': None,
            'previous': None,
            'results': serializer.data,
        })

    @extend_schema(
        responses={200: AdminFormularioSubmissionDetailSerializer},
        summary='Detalle individual de un envío de formulario (ADM)',
    )
    @action(detail=True, methods=['get'], url_path=r'submissions/(?P<submission_id>[^/.]+)')
    def submission_detail(self, request, pk=None, submission_id=None):
        formulario = self.get_object()
        try:
            sub_uuid = uuid.UUID(str(submission_id))
            envio = get_object_or_404(FormularioEnvio, formulario=formulario, pk=sub_uuid)
        except (ValueError, TypeError):
            raise ValidationError({'submission_id': 'El identificador de envío debe ser un UUID válido.'})

        AuditService.set_db_actor_session(request.user)
        AuditService.log(
            actor=request.user,
            action='read',
            module='formularios_dinamicos',
            target_model='formulario_envios',
            target_id=envio.id,
            description=f'Consulta administrativa detallada de envío {envio.id} en formulario "{formulario.titulo}"',
        )

        serializer = AdminFormularioSubmissionDetailSerializer(envio)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='submissions-export')
    def export_submissions(self, request, pk=None):
        formulario = self.get_object()
        version_num = request.query_params.get('version')
        v_int = int(version_num) if version_num and version_num.isdigit() else None

        csv_content = FormularioExportService.export_csv(formulario, v_int)
        v_tag = f'_v{v_int}' if v_int else ''
        filename = f'formulario_{formulario.slug}{v_tag}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv'

        AuditService.set_db_actor_session(request.user)
        AuditService.log(
            actor=request.user,
            action='export',
            module='formularios_dinamicos',
            target_model='formulario_envios',
            target_id=formulario.id,
            description=f'Exportación de respuestas en CSV del formulario "{formulario.titulo}"',
        )

        response = HttpResponse(csv_content, content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


# ---- Vistas Públicas ----

class PublicFormularioDetailView(APIView):
    """GET /api/v1/public/forms/{slug}/: Consulta del formulario vigente para el ciudadano."""
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicFormularioDetailSerializer

    def get(self, request, slug: str):
        formulario = get_object_or_404(Formulario, slug=slug, estado=Formulario.Estado.PUBLICADO)
        serializer = PublicFormularioDetailSerializer(formulario)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicFormularioSubmitView(APIView):
    """
    POST /api/v1/public/forms/{slug}/submit/: Envío público de respuestas.
    Exige la cabecera obligatoria Idempotency-Key.
    Respuesta neutral anti-enumeración.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicFormularioSubmitSerializer

    def post(self, request, slug: str):
        formulario = get_object_or_404(Formulario, slug=slug)

        idempotency_raw = request.headers.get('Idempotency-Key') or request.META.get('HTTP_IDEMPOTENCY_KEY')
        idempotency_uuid = validate_idempotency_key(idempotency_raw)

        serializer = PublicFormularioSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        envio = FormularioSubmissionService.process_submission(
            formulario=formulario,
            validated_data=serializer.validated_data,
            request=request,
            idempotency_key=idempotency_uuid,
        )

        return Response({
            'id_envio': str(envio.id),
            'estado': 'recibido',
            'mensaje': (
                'Tu formulario fue recibido correctamente. '
                'Si se requiere confirmar o activar el acceso, recibirás instrucciones en el correo indicado.'
            ),
        }, status=status.HTTP_201_CREATED)


class PublicActivationVerifyView(APIView):
    """POST /api/v1/public/forms/activation/verify/: Activación y fijación de contraseña."""
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicActivationVerifySerializer

    def post(self, request):
        serializer = PublicActivationVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        nueva_clave = serializer.validated_data['nueva_contrasena']
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1')).split(',')[0].strip()

        FormularioTokenService.verify_and_activate(token, nueva_clave, ip=ip)

        return Response({
            'mensaje': 'Cuenta activada exitosamente.',
            'estado': 'activada',
            'login_required': True,
        }, status=status.HTTP_200_OK)


class PublicActivationResendView(APIView):
    """POST /api/v1/public/forms/activation/resend/: Reenvío de token neutral."""
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicActivationResendSerializer

    def post(self, request):
        serializer = PublicActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        correo = serializer.validated_data['correo']
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1')).split(',')[0].strip()

        FormularioTokenService.resend_token(correo=correo, ip=ip)

        return Response({
            'mensaje': 'Si el correo tiene una solicitud pendiente de activación o confirmación, se ha enviado un nuevo enlace.',
        }, status=status.HTTP_200_OK)


# ---- Vistas Ciudadanas ----

class CitizenSubmissionListView(APIView):
    """GET /api/v1/me/forms/submissions/: Listado de formularios enviados por el ciudadano."""
    permission_classes = [IsCitizenOnly]
    serializer_class = CitizenSubmissionListSerializer

    def get(self, request):
        qs = FormularioEnvio.objects.filter(usuario=request.user).select_related('formulario', 'version').order_by('-fecha_envio')
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = CitizenSubmissionListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CitizenSubmissionDetailView(APIView):
    """GET /api/v1/me/forms/submissions/{id}/: Detalle histórico de un formulario enviado."""
    permission_classes = [IsCitizenOnly]
    serializer_class = CitizenSubmissionDetailSerializer

    def get(self, request, submission_id: str):
        envio = get_object_or_404(FormularioEnvio, pk=submission_id, usuario=request.user)
        serializer = CitizenSubmissionDetailSerializer(envio)
        return Response(serializer.data, status=status.HTTP_200_OK)
