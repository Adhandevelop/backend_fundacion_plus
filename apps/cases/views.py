from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Role, User
from apps.accounts.permissions import IsAdminOrSuperAdmin, IsCitizen, IsResponsibleOrAdmin
from apps.audit.services import AuditService
from apps.cases.models import Case, CaseCategory, CaseEvidence, CaseStatus
from apps.cases.serializers import (
    AdminCaseDetailSerializer,
    CaseAssignResponsibleSerializer,
    CaseCategorySerializer,
    CaseEvidenceSerializer,
    CaseManagementStatusSerializer,
    CaseModerationActionSerializer,
    CaseStatusSerializer,
    CaseUpdateCreateSerializer,
    CitizenCaseCreateUpdateSerializer,
    PublicCaseDetailSerializer,
    PublicCaseListSerializer,
)
from apps.cases.services import CaseService
from apps.tracking.serializers import CaseUpdateSerializer
from core.gis import parse_bbox


class PublicCaseCategoryListView(generics.ListAPIView):
    queryset = CaseCategory.objects.filter(activo=True)
    serializer_class = CaseCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class PublicCaseStatusListView(generics.ListAPIView):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class PublicCaseMapGeoJSONView(APIView):
    """
    GET /api/v1/public/cases/map/
    Retorna un GeoJSON FeatureCollection (SRID 4326) de los casos con `estado_publicacion='aprobado'`.
    Generaliza las coordenadas (`public_location`) para proteger ubicaciones sensibles (base de datos.md línea 60).
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = (
            Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO)
            .select_related('tipo_caso', 'comunidad', 'comunidad__municipio', 'estado')
            .order_by('-fecha_creacion')
        )

        params = request.query_params
        if muni := (params.get('municipio') or params.get('municipality')):
            qs = qs.filter(comunidad__municipio_id=muni)
        if comm := (params.get('comunidad') or params.get('community')):
            qs = qs.filter(comunidad_id=comm)
        if cat := (params.get('tipo_caso') or params.get('category')):
            qs = qs.filter(tipo_caso_id=cat)
        if est := (params.get('estado') or params.get('management_status')):
            qs = qs.filter(estado__nombre__iexact=est)

        bbox = None
        if bbox_str := params.get('bbox'):
            try:
                bbox = parse_bbox(bbox_str)
            except ValueError as exc:
                raise ValidationError({'bbox': str(exc)})

        features = []
        for c in qs[:500]:
            pub_loc = c.public_location
            if not pub_loc:
                continue
            lon, lat = pub_loc['coordinates']
            if bbox:
                min_lon, min_lat, max_lon, max_lat = bbox
                if not (float(min_lon) <= lon <= float(max_lon) and float(min_lat) <= lat <= float(max_lat)):
                    continue

            features.append({
                'type': 'Feature',
                'id': str(c.id),
                'geometry': pub_loc,
                'properties': {
                    'id_caso': str(c.id),
                    'codigo': c.codigo,
                    'radicado_code': c.codigo,
                    'titulo': c.titulo,
                    'prioridad': c.prioridad,
                    'estado': c.estado.nombre,
                    'tipo': c.tipo_caso.nombre,
                    'categoria': c.tipo_caso.categoria,
                    'comunidad': c.comunidad.nombre,
                    'municipio': c.comunidad.municipio.nombre,
                    'longitud': lon,
                    'latitud': lat,
                    'fecha_creacion': c.fecha_creacion.isoformat(),
                },
            })

        return Response({
            'type': 'FeatureCollection',
            'srid': 4326,
            'count': len(features),
            'features': features,
        })


class PublicCaseListView(generics.ListAPIView):
    serializer_class = PublicCaseListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = (
            Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO)
            .select_related('tipo_caso', 'comunidad', 'comunidad__municipio', 'estado')
            .order_by('-fecha_creacion')
        )
        params = self.request.query_params
        if muni := (params.get('municipio') or params.get('municipality')):
            qs = qs.filter(comunidad__municipio_id=muni)
        if comm := (params.get('comunidad') or params.get('community')):
            qs = qs.filter(comunidad_id=comm)
        if cat := (params.get('tipo_caso') or params.get('category')):
            qs = qs.filter(tipo_caso_id=cat)
        if search := params.get('search'):
            qs = qs.filter(titulo__icontains=search) | qs.filter(codigo__icontains=search)
        return qs


class PublicCaseDetailView(generics.RetrieveAPIView):
    serializer_class = PublicCaseDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        lookup = self.kwargs['lookup']
        qs = Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO).select_related(
            'tipo_caso', 'comunidad', 'comunidad__municipio', 'estado'
        )
        case = qs.filter(codigo__iexact=lookup).first()
        if not case:
            case = get_object_or_404(qs, pk=lookup)
        return case


class CitizenDashboardView(APIView):
    permission_classes = [IsCitizen]

    def get(self, request):
        my_cases = Case.objects.filter(usuario=request.user)
        unread_notifications = request.user.notificaciones.filter(leida=False).count()
        return Response({
            'total_cases': my_cases.count(),
            'pendientes_publicacion': my_cases.filter(estado_publicacion=Case.EstadoPublicacion.PENDIENTE).count(),
            'aprobados_publicacion': my_cases.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO).count(),
            'en_gestion': my_cases.filter(
                estado__nombre__in=[CaseStatus.Nombre.EN_REVISION, CaseStatus.Nombre.EN_PROCESO]
            ).count(),
            'resueltos_o_cerrados': my_cases.filter(
                estado__nombre__in=[CaseStatus.Nombre.RESUELTO, CaseStatus.Nombre.CERRADO]
            ).count(),
            'unread_notifications': unread_notifications,
        })


class CitizenCaseViewSet(viewsets.ModelViewSet):
    serializer_class = CitizenCaseCreateUpdateSerializer
    permission_classes = [IsCitizen]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        return (
            Case.objects.filter(usuario=self.request.user)
            .select_related('tipo_caso', 'comunidad', 'comunidad__municipio', 'estado')
            .prefetch_related('seguimientos', 'evidencias')
        )

    def perform_create(self, serializer):
        case = CaseService.register_case(
            reporter=self.request.user,
            validated_data=serializer.validated_data,
            request=self.request,
        )
        serializer.instance = case

    def perform_update(self, serializer):
        case = self.get_object()
        if case.estado_publicacion != Case.EstadoPublicacion.PENDIENTE:
            raise ValidationError('Solo puedes editar el caso mientras está en estado pendiente de revisión.')
        AuditService.set_db_actor_session(self.request.user)
        serializer.save()

    @action(detail=True, methods=['post'], url_path='evidence')
    def upload_evidence(self, request, pk=None):
        case = self.get_object()
        serializer = CaseEvidenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuditService.set_db_actor_session(request.user)
        evidence = serializer.save(caso=case, usuario=request.user)
        return Response(CaseEvidenceSerializer(evidence).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='updates')
    def add_additional_info(self, request, pk=None):
        case = self.get_object()
        serializer = CaseUpdateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seguimiento = CaseService.add_case_update(
            case=case,
            author=request.user,
            descripcion=serializer.validated_data['resolved_descripcion'],
            visible_publicamente=False,
            request=request,
        )
        return Response(CaseUpdateSerializer(seguimiento).data, status=status.HTTP_201_CREATED)


class AdminCaseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CaseCategory.objects.all()
    serializer_class = CaseCategorySerializer
    permission_classes = [IsAdminOrSuperAdmin]


class AdminCaseViewSet(viewsets.ModelViewSet):
    serializer_class = AdminCaseDetailSerializer
    permission_classes = [IsResponsibleOrAdmin]

    def get_queryset(self):
        user = self.request.user
        qs = (
            Case.objects.select_related('usuario', 'tipo_caso', 'comunidad', 'comunidad__municipio', 'estado')
            .prefetch_related('asignaciones__responsable', 'seguimientos', 'historial_estados', 'evidencias')
            .all()
        )
        if not user.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR):
            qs = qs.filter(asignaciones__responsable=user, asignaciones__activo=True).distinct()

        params = self.request.query_params
        if pub := (params.get('estado_publicacion') or params.get('moderation_status')):
            qs = qs.filter(estado_publicacion__iexact=pub)
        if est := (params.get('estado') or params.get('management_status')):
            qs = qs.filter(estado__nombre__iexact=est)
        if comm := (params.get('comunidad') or params.get('community')):
            qs = qs.filter(comunidad_id=comm)
        if cat := (params.get('tipo_caso') or params.get('category')):
            qs = qs.filter(tipo_caso_id=cat)
        return qs

    @action(detail=True, methods=['post'], url_path='moderate', permission_classes=[IsAdminOrSuperAdmin])
    def moderate(self, request, pk=None):
        case = self.get_object()
        serializer = CaseModerationActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_case = CaseService.moderate_case(
            case=case,
            actor=request.user,
            estado_publicacion=serializer.validated_data['resolved_pub'],
            motivo=serializer.validated_data['resolved_motivo'],
            prioridad=serializer.validated_data['resolved_prio'],
            request=request,
        )
        return Response(AdminCaseDetailSerializer(updated_case).data)

    @action(detail=True, methods=['post'], url_path='assign', permission_classes=[IsAdminOrSuperAdmin])
    def assign(self, request, pk=None):
        case = self.get_object()
        serializer = CaseAssignResponsibleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        responsable = get_object_or_404(
            User,
            pk=serializer.validated_data['resolved_responsable_id'],
            estado=User.Estado.ACTIVO,
        )
        CaseService.assign_responsible(
            case=case,
            actor=request.user,
            responsable=responsable,
            request=request,
        )
        case.refresh_from_db()
        return Response(AdminCaseDetailSerializer(case).data)

    @action(detail=True, methods=['post'], url_path='status')
    def change_status(self, request, pk=None):
        case = self.get_object()
        serializer = CaseManagementStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_case = CaseService.change_management_status(
            case=case,
            actor=request.user,
            new_status_name=serializer.validated_data['resolved_status'],
            motivo=serializer.validated_data['resolved_motivo'],
            request=request,
        )
        return Response(AdminCaseDetailSerializer(updated_case).data)

    @action(detail=True, methods=['post'], url_path='updates')
    def add_update(self, request, pk=None):
        case = self.get_object()
        serializer = CaseUpdateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seguimiento = CaseService.add_case_update(
            case=case,
            author=request.user,
            descripcion=serializer.validated_data['resolved_descripcion'],
            visible_publicamente=serializer.validated_data['resolved_visible'],
            request=request,
        )
        return Response(CaseUpdateSerializer(seguimiento).data, status=status.HTTP_201_CREATED)


class AdminCaseEvidenceViewSet(viewsets.ModelViewSet):
    queryset = CaseEvidence.objects.select_related('caso', 'usuario').all()
    serializer_class = CaseEvidenceSerializer
    permission_classes = [IsAdminOrSuperAdmin]
