import csv
import uuid as uuid_lib
from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage
from django.db.models import Count, Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, inline_serializer
from rest_framework import generics, permissions, serializers as drf_serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Role, User
from apps.accounts.permissions import (
    IsAdminOrSuperAdmin,
    IsCitizen,
    IsCitizenOnly,
    IsModeratorOrAdmin,
    IsResponsibleOrAdmin,
)
from apps.audit.services import AuditService
from apps.cases.models import (
    Case,
    CaseCategory,
    CaseEvidence,
    CaseStatus,
    FollowedCase,
)
from apps.cases.serializers import (
    AdminCaseDetailSerializer,
    CaseAssignResponsibleSerializer,
    CaseCategorySerializer,
    CaseContributionSerializer,
    CaseCorrectionRequestCreateSerializer,
    CaseCorrectionRequestSerializer,
    CaseEvidenceSerializer,
    CaseEvidenceUpdateSerializer,
    CaseManagementStatusSerializer,
    CaseModerationActionSerializer,
    CaseStatusSerializer,
    CaseUpdateCreateSerializer,
    CitizenCaseCreateUpdateSerializer,
    CitizenContributionCreateSerializer,
    FollowedCaseSerializer,
    GeoJSONCaseFeatureCollectionSerializer,
    PublicCaseDetailSerializer,
    PublicCaseListSerializer,
)
from apps.cases.services import CaseService
from apps.tracking.models import CaseUpdate
from apps.tracking.serializers import (
    CaseStatusHistorySerializer,
    CaseUpdateSerializer,
    PublicCaseStatusHistorySerializer,
    PublicCaseUpdateSerializer,
)
from core.gis import parse_bbox


def resolve_case_by_ref(queryset, ref: str) -> Case:
    """Permite buscar un caso tanto por su código de radicado (PLUS-YYYY-NNNNN) como por su UUID."""
    ref_str = str(ref).strip()
    by_code = queryset.filter(codigo__iexact=ref_str).first()
    if by_code:
        return by_code
    try:
        uuid_val = uuid_lib.UUID(ref_str)
        return get_object_or_404(queryset, pk=uuid_val)
    except (ValueError, TypeError):
        return get_object_or_404(queryset, codigo__iexact=ref_str)


class PublicCaseCategoryListView(generics.ListAPIView):
    queryset = CaseCategory.objects.filter(activo=True)
    serializer_class = CaseCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class PublicCaseCategoryNamesView(APIView):
    """
    CAT-05: GET /api/v1/catalogs/case-categories/
    Retorna valores distintos de `tipos_caso.categoria` (textos de hasta 50 caracteres) y los tipos activos.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='PublicCaseCategoryNamesResponse',
                fields={
                    'categories': drf_serializers.ListField(child=drf_serializers.CharField()),
                    'tipos_caso': CaseCategorySerializer(many=True),
                },
            )
        },
        summary='Categorías temáticas y tipos de caso activos (CAT-05)',
    )
    def get(self, request):
        active_types = CaseCategory.objects.filter(activo=True).order_by('categoria', 'nombre')
        categories = list(dict.fromkeys(active_types.values_list('categoria', flat=True)))
        return Response({
            'categories': categories,
            'tipos_caso': CaseCategorySerializer(active_types, many=True).data,
        })


class PublicCaseOptionsView(APIView):
    """
    CAT-06: GET /api/v1/catalogs/case-options/
    Retorna tipos_caso activos, estados_caso, prioridades, estados de publicación y naturalezas.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='PublicCaseOptionsResponse',
                fields={
                    'tipos_caso': CaseCategorySerializer(many=True),
                    'categorias': drf_serializers.ListField(child=drf_serializers.CharField()),
                    'estados_caso': CaseStatusSerializer(many=True),
                    'prioridades': drf_serializers.ListField(child=drf_serializers.DictField()),
                    'estados_publicacion': drf_serializers.ListField(child=drf_serializers.DictField()),
                    'naturalezas': drf_serializers.ListField(child=drf_serializers.DictField()),
                    'audiencias_seguimiento': drf_serializers.ListField(child=drf_serializers.DictField()),
                    'tipos_evento_seguimiento': drf_serializers.ListField(child=drf_serializers.DictField()),
                },
            )
        },
        summary='Opciones maestras de casos: tipos, estados, prioridades y audiencias (CAT-06)',
    )
    def get(self, request):
        active_types = CaseCategory.objects.filter(activo=True).order_by('categoria', 'nombre')
        statuses = CaseStatus.objects.all().order_by('orden')
        categories = list(dict.fromkeys(active_types.values_list('categoria', flat=True)))
        return Response({
            'tipos_caso': CaseCategorySerializer(active_types, many=True).data,
            'categorias': categories,
            'estados_caso': CaseStatusSerializer(statuses, many=True).data,
            'prioridades': [{'value': k, 'label': v} for k, v in Case.Prioridad.choices],
            'estados_publicacion': [{'value': k, 'label': v} for k, v in Case.EstadoPublicacion.choices],
            'naturalezas': [{'value': k, 'label': v} for k, v in CaseCategory.Naturaleza.choices],
            'audiencias_seguimiento': [{'value': k, 'label': v} for k, v in CaseUpdate.Audiencia.choices],
            'tipos_evento_seguimiento': [{'value': k, 'label': v} for k, v in CaseUpdate.TipoEvento.choices],
        })


class PublicCaseStatusListView(generics.ListAPIView):
    queryset = CaseStatus.objects.all()
    serializer_class = CaseStatusSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


def apply_public_case_filters(qs, params):
    if dept := (params.get('id_departamento') or params.get('departamento') or params.get('department')):
        qs = qs.filter(comunidad__municipio__departamento_id=dept)
    if muni := (params.get('id_municipio') or params.get('municipio') or params.get('municipality')):
        qs = qs.filter(comunidad__municipio_id=muni)
    if comm := (params.get('id_comunidad') or params.get('comunidad') or params.get('community')):
        qs = qs.filter(comunidad_id=comm)
    if cat := (params.get('id_tipo_caso') or params.get('tipo_caso') or params.get('category')):
        qs = qs.filter(tipo_caso_id=cat)
    if cat_text := params.get('categoria'):
        qs = qs.filter(tipo_caso__categoria__iexact=cat_text)
    if nat := params.get('naturaleza'):
        qs = qs.filter(tipo_caso__naturaleza__iexact=nat)
    if est_id := params.get('id_estado'):
        qs = qs.filter(estado_id=est_id)
    elif est := (params.get('estado') or params.get('management_status')):
        qs = qs.filter(estado__nombre__iexact=est)
    if prio := params.get('prioridad'):
        qs = qs.filter(prioridad__iexact=prio)
    if search := params.get('search'):
        qs = qs.filter(Q(titulo__icontains=search) | Q(codigo__icontains=search) | Q(descripcion__icontains=search))
    return qs


class PublicCaseMapGeoJSONView(APIView):
    """
    MAP-02: GET /api/v1/public/cases/map/ (y /api/v1/public/cases/geojson/)
    Retorna un GeoJSON FeatureCollection (SRID 4326) de los casos con `estado_publicacion='aprobado'`.
    Generaliza las coordenadas (`public_location`) para proteger ubicaciones sensibles (base de datos.md línea 60).
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = GeoJSONCaseFeatureCollectionSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter('bbox', OpenApiTypes.STR, description='Bounding box: minLon,minLat,maxLon,maxLat (SRID 4326)'),
            OpenApiParameter('id_departamento', OpenApiTypes.UUID, description='Filtrar por departamento'),
            OpenApiParameter('id_municipio', OpenApiTypes.UUID, description='Filtrar por municipio'),
            OpenApiParameter('id_comunidad', OpenApiTypes.UUID, description='Filtrar por comunidad'),
            OpenApiParameter('id_tipo_caso', OpenApiTypes.UUID, description='Filtrar por tipo de caso'),
            OpenApiParameter('categoria', OpenApiTypes.STR, description='Filtrar por categoría temática textual'),
            OpenApiParameter('naturaleza', OpenApiTypes.STR, description='Filtrar por naturaleza (problematica, proyecto_iniciativa, otro)'),
            OpenApiParameter('id_estado', OpenApiTypes.UUID, description='Filtrar por UUID de estado operativo'),
            OpenApiParameter('estado', OpenApiTypes.STR, description='Filtrar por nombre de estado operativo'),
            OpenApiParameter('prioridad', OpenApiTypes.STR, description='Filtrar por prioridad (baja, media, alta, critica)'),
            OpenApiParameter('search', OpenApiTypes.STR, description='Búsqueda por código, título o descripción'),
        ],
        responses={200: GeoJSONCaseFeatureCollectionSerializer},
        summary='Capa GeoJSON FeatureCollection de casos públicos aprobados (MAP-02)',
    )
    def get(self, request):
        qs = (
            Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO)
            .select_related('tipo_caso', 'comunidad', 'comunidad__municipio', 'comunidad__municipio__departamento', 'estado')
            .order_by('-fecha_creacion')
        )
        qs = apply_public_case_filters(qs, request.query_params)

        bbox = None
        if bbox_str := request.query_params.get('bbox'):
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
                    'id_estado': str(c.estado_id),
                    'estado': c.estado.nombre,
                    'id_tipo_caso': str(c.tipo_caso_id),
                    'tipo': c.tipo_caso.nombre,
                    'categoria': c.tipo_caso.categoria,
                    'naturaleza': c.tipo_caso.naturaleza,
                    'id_comunidad': str(c.comunidad_id),
                    'comunidad': c.comunidad.nombre,
                    'id_municipio': str(c.comunidad.municipio_id),
                    'municipio': c.comunidad.municipio.nombre,
                    'id_departamento': str(c.comunidad.municipio.departamento_id),
                    'departamento': c.comunidad.municipio.departamento.nombre,
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
    """MAP-01: GET /api/v1/public/cases/"""
    serializer_class = PublicCaseListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = (
            Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO)
            .select_related('tipo_caso', 'comunidad', 'comunidad__municipio', 'comunidad__municipio__departamento', 'estado')
            .order_by('-fecha_creacion')
        )
        return apply_public_case_filters(qs, self.request.query_params)


class PublicCaseDetailView(generics.RetrieveAPIView):
    """MAP-03: GET /api/v1/public/cases/{case_ref}/"""
    serializer_class = PublicCaseDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        lookup = self.kwargs['lookup']
        qs = Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO).select_related(
            'tipo_caso', 'comunidad', 'comunidad__municipio', 'comunidad__municipio__departamento', 'estado'
        )
        return resolve_case_by_ref(qs, lookup)


class PublicCaseHistoryView(APIView):
    """
    MAP-04: GET /api/v1/public/cases/{case_id}/history/
    Solo entrega seguimientos con `visible_publicamente=True` (audiencia='publico') y cambios de estado del caso aprobado.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='PublicCaseHistoryResponse',
                fields={
                    'id_caso': drf_serializers.UUIDField(),
                    'codigo': drf_serializers.CharField(),
                    'seguimientos': PublicCaseUpdateSerializer(many=True),
                    'historial_estados': PublicCaseStatusHistorySerializer(many=True),
                },
            )
        },
        summary='Historial público de seguimientos autorizados y cambios de estado (MAP-04)',
    )
    def get(self, request, case_id):
        qs = Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO)
        case = resolve_case_by_ref(qs, case_id)
        updates = case.seguimientos.filter(visible_publicamente=True)
        status_history = case.historial_estados.select_related('estado_anterior', 'estado_nuevo').all()
        return Response({
            'id_caso': str(case.id),
            'codigo': case.codigo,
            'seguimientos': PublicCaseUpdateSerializer(updates, many=True).data,
            'historial_estados': PublicCaseStatusHistorySerializer(status_history, many=True).data,
        })


class PublicCaseEvidenceView(APIView):
    """
    MAP-05: GET /api/v1/public/cases/{case_id}/evidence/
    Solo entrega evidencias expresamente marcadas como `audiencia='publico'` y `estado_revision='aprobada'`.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={200: CaseEvidenceSerializer(many=True)},
        summary='Listado de evidencias públicas aprobadas de un caso (MAP-05)',
    )
    def get(self, request, case_id):
        qs = Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO)
        case = resolve_case_by_ref(qs, case_id)
        evidencias = case.evidencias.filter(
            audiencia=CaseEvidence.Audiencia.PUBLICO,
            estado_revision=CaseEvidence.EstadoRevision.APROBADA,
        )
        return Response(CaseEvidenceSerializer(evidencias, many=True).data)


class FollowedCaseView(APIView):
    """
    MAP-08, MAP-09, MAP-10 (AMP-03):
    GET / PUT / DELETE /api/v1/me/followed-cases/{case_id}/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowedCaseSerializer

    def _get_followable_case(self, case_id) -> Case:
        qs = Case.objects.filter(
            Q(estado_publicacion=Case.EstadoPublicacion.APROBADO) | Q(usuario=self.request.user)
        )
        return resolve_case_by_ref(qs, case_id)

    def get(self, request, case_id=None):
        if not case_id:
            follows = FollowedCase.objects.filter(usuario=request.user, activo=True).select_related('caso')
            data = FollowedCaseSerializer(follows, many=True).data
            return Response({'count': len(data), 'results': data})
        case = self._get_followable_case(case_id)
        follow = FollowedCase.objects.filter(usuario=request.user, caso=case).first()
        return Response({
            'id_caso': str(case.id),
            'followed': bool(follow and follow.activo),
            'detail': FollowedCaseSerializer(follow).data if follow else None,
        })

    def post(self, request, case_id):
        return self.put(request, case_id)

    def put(self, request, case_id):
        case = self._get_followable_case(case_id)
        follow, created = FollowedCase.objects.get_or_create(
            usuario=request.user,
            caso=case,
            defaults={'activo': True},
        )
        if not created and not follow.activo:
            follow.activo = True
            follow.fecha_baja = None
            follow.save(update_fields=['activo', 'fecha_baja'])
        return Response(FollowedCaseSerializer(follow).data, status=status.HTTP_200_OK)

    def delete(self, request, case_id):
        case = self._get_followable_case(case_id)
        FollowedCase.objects.filter(usuario=request.user, caso=case, activo=True).update(
            activo=False,
            fecha_baja=timezone.now(),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminFollowedCaseView(APIView):
    """
    Gestión de casos seguidos para cuentas institucionales / administrativas (IsResponsibleOrAdmin).
    Permite consultar, seguir y dejar de seguir casos públicos sin usar rutas ciudadanas /me.
    """
    serializer_class = FollowedCaseSerializer
    permission_classes = [IsResponsibleOrAdmin]

    def _get_followable_case(self, case_id) -> Case:
        qs = Case.objects.filter(
            Q(estado_publicacion=Case.EstadoPublicacion.APROBADO) | Q(usuario=self.request.user)
        )
        return resolve_case_by_ref(qs, case_id)

    @extend_schema(
        summary="Listar casos seguidos por la cuenta administrativa autenticada",
        description=(
            "Retorna la colección de casos que el usuario institucional autenticado "
            "ha marcado para seguimiento. Solo incluye registros activos."
        ),
        responses={200: FollowedCaseSerializer(many=True)},
    )
    def get(self, request, case_id=None):
        if not case_id:
            follows = (
                FollowedCase.objects.filter(usuario=request.user, activo=True)
                .select_related(
                    'caso',
                    'caso__estado',
                    'caso__comunidad',
                    'caso__tipo_caso',
                )
                .order_by('-fecha_creacion')
            )
            data = FollowedCaseSerializer(follows, many=True).data
            return Response({'count': len(data), 'results': data})

        case = self._get_followable_case(case_id)
        follow = FollowedCase.objects.filter(usuario=request.user, caso=case).first()
        return Response({
            'id_caso': str(case.id),
            'followed': bool(follow and follow.activo),
            'detail': FollowedCaseSerializer(follow).data if follow else None,
        })

    @extend_schema(
        summary="Seguir un caso (cuenta institucional)",
        description=(
            "Activa el seguimiento sobre un caso público aprobado o propio. "
            "Si ya existía un seguimiento previo desactivado, lo reactiva. "
            "Acepta el identificador en la URL o en el cuerpo JSON: {'caso': '{uuid}'}."
        ),
        responses={200: FollowedCaseSerializer},
    )
    def post(self, request, case_id=None):
        target_id = case_id or request.data.get('caso') or request.data.get('id_caso') or request.data.get('case_id')
        if not target_id:
            raise ValidationError({'caso': 'Debe especificar el identificador del caso a seguir.'})
        return self.put(request, target_id)

    @extend_schema(
        summary="Actualizar o activar seguimiento de un caso (cuenta institucional)",
        responses={200: FollowedCaseSerializer},
    )
    def put(self, request, case_id):
        case = self._get_followable_case(case_id)
        follow, created = FollowedCase.objects.get_or_create(
            usuario=request.user,
            caso=case,
            defaults={'activo': True},
        )
        if not created and not follow.activo:
            follow.activo = True
            follow.fecha_baja = None
            follow.save(update_fields=['activo', 'fecha_baja'])
        return Response(FollowedCaseSerializer(follow).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Dejar de seguir un caso (desactivación lógica)",
        description="Desactiva el seguimiento estableciendo activo=False y registrando fecha_baja. El registro se preserva para auditoría.",
        responses={204: None},
    )
    def delete(self, request, case_id):
        case = self._get_followable_case(case_id)
        FollowedCase.objects.filter(usuario=request.user, caso=case, activo=True).update(
            activo=False,
            fecha_baja=timezone.now(),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CitizenDashboardView(APIView):
    """CIT-01: GET /api/v1/me/dashboard/ (y /api/v1/citizen/dashboard/)"""
    permission_classes = [IsCitizenOnly]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='CitizenDashboardResponse',
                fields={
                    'total_cases': drf_serializers.IntegerField(),
                    'pendientes_publicacion': drf_serializers.IntegerField(),
                    'aprobados_publicacion': drf_serializers.IntegerField(),
                    'en_gestion': drf_serializers.IntegerField(),
                    'resueltos_o_cerrados': drf_serializers.IntegerField(),
                    'open_correction_requests': drf_serializers.IntegerField(),
                    'unread_notifications': drf_serializers.IntegerField(),
                    'unread_messages': drf_serializers.IntegerField(),
                    'followed_cases_count': drf_serializers.IntegerField(),
                },
            )
        },
        summary='Resumen del panel ciudadano autenticado (CIT-01)',
    )
    def get(self, request):
        my_cases = Case.objects.filter(usuario=request.user)
        unread_notifications = request.user.notificaciones.filter(leida=False).count()
        unread_messages = request.user.mensajes_recibidos.filter(fecha_lectura__isnull=True).count()
        open_corrections = sum(
            1 for c in my_cases.prefetch_related('solicitudes_correccion') if c.active_correction_request
        )
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
            'open_correction_requests': open_corrections,
            'unread_notifications': unread_notifications,
            'unread_messages': unread_messages,
            'followed_cases_count': FollowedCase.objects.filter(usuario=request.user, activo=True).count(),
        })


class CitizenCaseViewSet(viewsets.ModelViewSet):
    """
    CIT-02 a CIT-08: Gestión de casos propios del ciudadano (`/api/v1/me/cases/` y `/api/v1/citizen/cases/`).
    Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
    """
    serializer_class = CitizenCaseCreateUpdateSerializer
    permission_classes = [IsCitizenOnly]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = (
            Case.objects.filter(usuario=self.request.user)
            .select_related('tipo_caso', 'comunidad', 'comunidad__municipio', 'comunidad__municipio__departamento', 'estado')
            .prefetch_related('seguimientos', 'evidencias', 'solicitudes_correccion', 'aportes__evidencias')
        )
        params = self.request.query_params
        if est := params.get('estado'):
            qs = qs.filter(estado__nombre__iexact=est)
        if pub := params.get('estado_publicacion'):
            qs = qs.filter(estado_publicacion__iexact=pub)
        if search := params.get('search'):
            qs = qs.filter(Q(titulo__icontains=search) | Q(codigo__icontains=search))
        return qs

    def get_object(self):
        lookup = self.kwargs.get(self.lookup_field)
        case = resolve_case_by_ref(self.get_queryset(), lookup)
        self.check_object_permissions(self.request, case)
        return case

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

    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        """
        CIT-05: GET /api/v1/me/cases/{case_id}/history/
        Compone seguimientos autorizados al ciudadano (`publico` o `ciudadano`, nunca `interno`),
        cambios de estado y aportes ciudadanos.
        """
        case = self.get_object()
        updates = case.seguimientos.filter(
            audiencia__in=[CaseUpdate.Audiencia.PUBLICO, CaseUpdate.Audiencia.CIUDADANO]
        )
        status_history = case.historial_estados.select_related('estado_anterior', 'estado_nuevo').all()
        contributions = case.aportes.prefetch_related('evidencias').all()
        return Response({
            'id_caso': str(case.id),
            'codigo': case.codigo,
            'seguimientos': CaseUpdateSerializer(updates, many=True, context={'request': request}).data,
            'historial_estados': PublicCaseStatusHistorySerializer(status_history, many=True).data,
            'aportes': CaseContributionSerializer(contributions, many=True).data,
            'solicitudes_correccion': [
                {
                    'id_solicitud': str(s.id),
                    'motivo': s.motivo,
                    'estado': s.estado,
                    'respuesta': s.respuesta,
                    'fecha_solicitud': s.fecha_solicitud,
                    'fecha_respuesta': s.fecha_respuesta,
                }
                for s in case.solicitudes_correccion.all()
            ],
        })

    @action(detail=True, methods=['get'], url_path='timeline')
    def timeline(self, request, pk=None):
        """Alias compatible con GET /api/v1/me/cases/{case_id}/timeline/"""
        return self.history(request, pk=pk)

    @extend_schema(
        request=CaseEvidenceSerializer,
        responses={200: CaseEvidenceSerializer(many=True), 201: CaseEvidenceSerializer},
        summary='Listar o subir evidencias del caso ciudadano (CIT-06)',
    )
    @action(detail=True, methods=['get', 'post'], url_path='evidence')
    def evidence(self, request, pk=None):
        """CIT-06: GET / POST /api/v1/me/cases/{case_id}/evidence/"""
        case = self.get_object()
        if request.method == 'GET':
            evidencias = case.evidencias.exclude(audiencia=CaseEvidence.Audiencia.PRIVADO)
            return Response(CaseEvidenceSerializer(evidencias, many=True).data)

        serializer = CaseEvidenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuditService.set_db_actor_session(request.user)
        evidence = serializer.save(
            caso=case,
            usuario=request.user,
            audiencia=CaseEvidence.Audiencia.CIUDADANO,
            estado_revision=CaseEvidence.EstadoRevision.PENDIENTE,
        )
        return Response(CaseEvidenceSerializer(evidence).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter('download', OpenApiTypes.BOOL, description='Si es 1/true, descarga el binario directamente (FileResponse).'),
        ],
        responses={200: CaseEvidenceSerializer},
        summary='Descargar o consultar metadatos protegidos de una evidencia (CIT-07)',
    )
    @action(detail=True, methods=['get'], url_path=r'evidence/(?P<evidence_id>[^/.]+)/download')
    def download_evidence(self, request, pk=None, evidence_id=None):
        """CIT-07: GET /api/v1/me/cases/{case_id}/evidence/{evidence_id}/download/"""
        case = self.get_object()
        ev = get_object_or_404(
            CaseEvidence.objects.exclude(audiencia=CaseEvidence.Audiencia.PRIVADO),
            pk=evidence_id,
            caso=case,
        )
        if request.query_params.get('download') in ('1', 'true') and ev.ruta_archivo and default_storage.exists(ev.ruta_archivo):
            return FileResponse(
                default_storage.open(ev.ruta_archivo, 'rb'),
                as_attachment=True,
                filename=ev.nombre_original or f'evidencia_{ev.id}',
                content_type=ev.mime_type or 'application/octet-stream',
            )
        return Response({
            'id_evidencia': str(ev.id),
            'id_caso': str(case.id),
            'nombre_original': ev.nombre_original,
            'tipo_archivo': ev.tipo_archivo,
            'mime_type': ev.mime_type,
            'tamano_bytes': ev.tamano_bytes,
            'ruta_archivo': ev.ruta_archivo,
            'download_url': f'/api/v1/me/cases/{case.id}/evidence/{ev.id}/download/?download=1',
        })

    @extend_schema(
        request=CitizenContributionCreateSerializer,
        responses={200: CaseContributionSerializer(many=True), 201: CaseContributionSerializer},
        summary='Listar o registrar aportes ciudadanos y respuestas a corrección (CIT-08)',
    )
    @action(detail=True, methods=['get', 'post'], url_path='contributions')
    def contributions(self, request, pk=None):
        """CIT-08 (AMP-07): GET / POST /api/v1/me/cases/{case_id}/contributions/"""
        case = self.get_object()
        if request.method == 'GET':
            qs = case.aportes.prefetch_related('evidencias').all()
            return Response(CaseContributionSerializer(qs, many=True).data)

        contenido = (
            request.data.get('contenido')
            or request.data.get('descripcion')
            or request.data.get('mensaje')
            or request.data.get('text')
            or ''
        ).strip()
        if not contenido:
            raise ValidationError({'contenido': 'El contenido del aporte ciudadano es obligatorio.'})
        files = request.FILES.getlist('files') or request.FILES.getlist('archivos')
        contribution = CaseService.add_citizen_contribution(
            case=case,
            author=request.user,
            contenido=contenido,
            solicitud_correccion_id=request.data.get('id_solicitud_correccion'),
            files=files,
            request=request,
        )
        return Response(CaseContributionSerializer(contribution).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='updates')
    def add_additional_info(self, request, pk=None):
        case = self.get_object()
        serializer = CaseUpdateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seguimiento = CaseService.add_case_update(
            case=case,
            author=request.user,
            titulo=serializer.validated_data['resolved_titulo'],
            descripcion=serializer.validated_data['resolved_descripcion'],
            audiencia=CaseUpdate.Audiencia.CIUDADANO,
            visible_publicamente=False,
            request=request,
        )
        return Response(CaseUpdateSerializer(seguimiento).data, status=status.HTTP_201_CREATED)


class AdminCaseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CaseCategory.objects.all()
    serializer_class = CaseCategorySerializer
    permission_classes = [IsAdminOrSuperAdmin]


def apply_admin_case_filters(qs, params, user=None):
    if user and (created_by_me := (params.get('created_by_me') or params.get('mine') or params.get('creados_por_mi'))):
        if str(created_by_me).strip().lower() in {'true', '1', 'yes'}:
            qs = qs.filter(usuario=user)
    if created_by := (params.get('created_by') or params.get('creado_por') or params.get('id_usuario')):
        qs = qs.filter(usuario_id=created_by)
    if pub := (params.get('estado_publicacion') or params.get('moderation_status')):
        qs = qs.filter(estado_publicacion__iexact=pub)
    if est_id := params.get('id_estado'):
        qs = qs.filter(estado_id=est_id)
    elif est := (params.get('estado') or params.get('management_status')):
        qs = qs.filter(estado__nombre__iexact=est)
    if prio := params.get('prioridad'):
        qs = qs.filter(prioridad__iexact=prio)
    if dept := (params.get('id_departamento') or params.get('departamento')):
        qs = qs.filter(comunidad__municipio__departamento_id=dept)
    if muni := (params.get('id_municipio') or params.get('municipio')):
        qs = qs.filter(comunidad__municipio_id=muni)
    if comm := (params.get('id_comunidad') or params.get('comunidad') or params.get('community')):
        qs = qs.filter(comunidad_id=comm)
    if cat := (params.get('id_tipo_caso') or params.get('tipo_caso') or params.get('category')):
        qs = qs.filter(tipo_caso_id=cat)
    if cat_text := params.get('categoria'):
        qs = qs.filter(tipo_caso__categoria__iexact=cat_text)
    if nat := params.get('naturaleza'):
        qs = qs.filter(tipo_caso__naturaleza__iexact=nat)
    if resp := (params.get('id_responsable') or params.get('responsable')):
        qs = qs.filter(asignaciones__responsable_id=resp, asignaciones__activo=True)
    if search := params.get('search'):
        qs = qs.filter(
            Q(codigo__icontains=search)
            | Q(titulo__icontains=search)
            | Q(descripcion__icontains=search)
        )
    return qs


class AdminCaseViewSet(viewsets.ModelViewSet):
    """
    ADM-02 a ADM-11: Gestión administrativa de casos (`/api/v1/admin/cases/`).
    Soporta lectura tanto por UUID como por código de radicado (`{case_ref}`).
    """
    serializer_class = AdminCaseDetailSerializer
    permission_classes = [IsResponsibleOrAdmin]

    def get_queryset(self):
        user = self.request.user
        qs = (
            Case.objects.select_related(
                'usuario',
                'tipo_caso',
                'comunidad',
                'comunidad__municipio',
                'comunidad__municipio__departamento',
                'estado',
            )
            .prefetch_related(
                'asignaciones__responsable',
                'seguimientos',
                'historial_estados',
                'evidencias',
                'solicitudes_correccion',
                'aportes__evidencias',
            )
            .all()
        )
        created_by_me = (
            self.request.query_params.get('created_by_me')
            or self.request.query_params.get('mine')
            or self.request.query_params.get('creados_por_mi')
        )
        is_created_by_me = str(created_by_me).strip().lower() in {'true', '1', 'yes'}

        if not user.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR):
            if is_created_by_me:
                qs = qs.filter(usuario=user)
            else:
                qs = qs.filter(
                    Q(asignaciones__responsable=user, asignaciones__activo=True) | Q(usuario=user)
                ).distinct()

        return apply_admin_case_filters(qs, self.request.query_params, user=user)

    @extend_schema(
        summary="Listar casos en el panel administrativo",
        description=(
            "Listado administrativo de casos. Permite filtrar por ?created_by_me=true "
            "(o ?mine=true) para consultar los casos creados por la cuenta autenticada ('Mis Casos')."
        ),
        parameters=[
            OpenApiParameter('created_by_me', OpenApiTypes.BOOL, OpenApiParameter.QUERY, required=False, description='Filtrar casos creados por el usuario autenticado (soporta alias mine=true).'),
            OpenApiParameter('created_by', OpenApiTypes.UUID, OpenApiParameter.QUERY, required=False, description='Filtrar por UUID del usuario creador (soporta creado_por).'),
            OpenApiParameter('estado_publicacion', OpenApiTypes.STR, OpenApiParameter.QUERY, required=False, description='Estado de publicación: pendiente, aprobado, rechazado.'),
            OpenApiParameter('id_estado', OpenApiTypes.UUID, OpenApiParameter.QUERY, required=False, description='UUID del estado de gestión.'),
            OpenApiParameter('estado', OpenApiTypes.STR, OpenApiParameter.QUERY, required=False, description='Nombre del estado de gestión.'),
            OpenApiParameter('prioridad', OpenApiTypes.STR, OpenApiParameter.QUERY, required=False, description='Prioridad: baja, media, alta, critica.'),
            OpenApiParameter('search', OpenApiTypes.STR, OpenApiParameter.QUERY, required=False, description='Búsqueda textual por código, título o descripción.'),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_object(self):
        lookup = self.kwargs.get(self.lookup_field)
        case = resolve_case_by_ref(self.get_queryset(), lookup)
        self.check_object_permissions(self.request, case)
        return case

    def perform_create(self, serializer):
        """Sección 14: Radicación institucional POST /api/v1/admin/cases/"""
        AuditService.set_db_actor_session(self.request.user)
        reporter = serializer.validated_data.get('usuario') or self.request.user
        case = serializer.save(usuario=reporter)
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='casos',
            target_model='casos',
            target_id=case.pk,
            description=f'Radicación administrativa de caso "{case.titulo}" ({case.codigo})',
            request=self.request,
        )

    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        """ADM-04: GET /api/v1/admin/cases/{case_id}/history/"""
        case = self.get_object()
        return Response({
            'id_caso': str(case.id),
            'codigo': case.codigo,
            'seguimientos': CaseUpdateSerializer(case.seguimientos.all(), many=True, context={'request': request}).data,
            'historial_estados': CaseStatusHistorySerializer(case.historial_estados.all(), many=True).data,
            'asignaciones': [
                {
                    'id_asignacion_caso': str(a.id),
                    'responsable': str(a.responsable_id),
                    'responsable_nombre': a.responsable.full_name,
                    'asignador_nombre': a.asignador.full_name,
                    'activo': a.activo,
                    'fecha_asignacion': a.fecha_asignacion,
                    'fecha_finalizacion': a.fecha_finalizacion,
                }
                for a in case.asignaciones.select_related('responsable', 'asignador').all()
            ],
            'solicitudes_correccion': [
                {
                    'id_solicitud': str(s.id),
                    'motivo': s.motivo,
                    'estado': s.estado,
                    'respuesta': s.respuesta,
                    'fecha_solicitud': s.fecha_solicitud,
                    'fecha_respuesta': s.fecha_respuesta,
                }
                for s in case.solicitudes_correccion.all()
            ],
            'aportes': CaseContributionSerializer(case.aportes.prefetch_related('evidencias').all(), many=True).data,
        })

    @action(detail=True, methods=['get'], url_path='timeline')
    def timeline(self, request, pk=None):
        """Alias compatible con GET /api/v1/me/cases/{case_id}/timeline/"""
        return self.history(request, pk=pk)

    @extend_schema(
        request=CaseEvidenceSerializer,
        responses={200: CaseEvidenceSerializer(many=True), 201: CaseEvidenceSerializer},
        summary='Listar o subir evidencias desde el panel administrativo (ADM-05)',
    )
    @action(detail=True, methods=['get', 'post'], url_path='evidence')
    def evidence(self, request, pk=None):
        """ADM-05: GET / POST /api/v1/admin/cases/{case_id}/evidence/"""
        case = self.get_object()
        if request.method == 'GET':
            return Response(CaseEvidenceSerializer(case.evidencias.all(), many=True).data)
        serializer = CaseEvidenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuditService.set_db_actor_session(request.user)
        ev = serializer.save(caso=case, usuario=request.user)
        return Response(CaseEvidenceSerializer(ev).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=CaseEvidenceUpdateSerializer,
        responses={200: CaseEvidenceSerializer},
        summary='Actualizar audiencia, estado de revisión o descripción de evidencia (ADM-11)',
    )
    @action(detail=True, methods=['patch'], url_path=r'evidence/(?P<evidence_id>[^/.]+)')
    def update_evidence(self, request, pk=None, evidence_id=None):
        """ADM-11 (AMP-10): PATCH /api/v1/admin/cases/{case_id}/evidence/{evidence_id}/"""
        case = self.get_object()
        ev = get_object_or_404(CaseEvidence, pk=evidence_id, caso=case)
        serializer = CaseEvidenceUpdateSerializer(ev, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        AuditService.set_db_actor_session(request.user)
        serializer.save()
        return Response(CaseEvidenceSerializer(ev).data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter('download', OpenApiTypes.BOOL, description='Si es 1/true, descarga el binario directamente (FileResponse).'),
        ],
        responses={200: CaseEvidenceSerializer},
        summary='Descargar o consultar metadatos protegidos de una evidencia (ADM-06)',
    )
    @action(detail=True, methods=['get'], url_path=r'evidence/(?P<evidence_id>[^/.]+)/download')
    def download_evidence(self, request, pk=None, evidence_id=None):
        """ADM-06: GET /api/v1/admin/cases/{case_id}/evidence/{evidence_id}/download/"""
        case = self.get_object()
        ev = get_object_or_404(CaseEvidence, pk=evidence_id, caso=case)
        if request.query_params.get('download') in ('1', 'true') and ev.ruta_archivo and default_storage.exists(ev.ruta_archivo):
            return FileResponse(
                default_storage.open(ev.ruta_archivo, 'rb'),
                as_attachment=True,
                filename=ev.nombre_original or f'evidencia_{ev.id}',
                content_type=ev.mime_type or 'application/octet-stream',
            )
        return Response({
            'id_evidencia': str(ev.id),
            'id_caso': str(case.id),
            'nombre_original': ev.nombre_original,
            'tipo_archivo': ev.tipo_archivo,
            'mime_type': ev.mime_type,
            'tamano_bytes': ev.tamano_bytes,
            'audiencia': ev.audiencia,
            'estado_revision': ev.estado_revision,
            'ruta_archivo': ev.ruta_archivo,
            'download_url': f'/api/v1/admin/cases/{case.id}/evidence/{ev.id}/download/?download=1',
        })

    def _handle_moderation(self, request):
        case = self.get_object()
        serializer = CaseModerationActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_case = CaseService.moderate_case(
            case=case,
            actor=request.user,
            estado_publicacion=serializer.validated_data['resolved_pub'],
            motivo=serializer.validated_data['resolved_motivo'],
            prioridad=serializer.validated_data['resolved_prio'],
            solicitar_correccion=serializer.validated_data['resolved_solicitar_correccion'],
            request=request,
        )
        return Response(AdminCaseDetailSerializer(updated_case, context={'request': request}).data)

    @extend_schema(
        request=CaseModerationActionSerializer,
        responses={200: AdminCaseDetailSerializer},
        summary='Aprobar, rechazar o solicitar corrección sobre la publicación de un caso (ADM-07)',
    )
    @action(detail=True, methods=['post'], url_path='moderation', permission_classes=[IsModeratorOrAdmin])
    def moderation(self, request, pk=None):
        """ADM-07: POST /api/v1/admin/cases/{case_id}/moderation/"""
        return self._handle_moderation(request)

    @extend_schema(
        request=CaseModerationActionSerializer,
        responses={200: AdminCaseDetailSerializer},
        summary='Alias compatible para moderar publicación de caso (ADM-07)',
    )
    @action(detail=True, methods=['post'], url_path='moderate', permission_classes=[IsModeratorOrAdmin])
    def moderate(self, request, pk=None):
        """Alias compatible con POST /api/v1/admin/cases/{case_id}/moderate/"""
        return self._handle_moderation(request)

    @extend_schema(
        request=CaseCorrectionRequestCreateSerializer,
        responses={201: CaseCorrectionRequestSerializer},
        summary='Crear solicitud formal de corrección para el ciudadano (ADM-07)',
    )
    @action(detail=True, methods=['post'], url_path='correction-requests', permission_classes=[IsModeratorOrAdmin])
    def correction_requests(self, request, pk=None):
        """ADM-07: POST /api/v1/admin/cases/{case_id}/correction-requests/"""
        case = self.get_object()
        motivo = (request.data.get('motivo') or request.data.get('moderation_reason') or '').strip()
        if not motivo:
            raise ValidationError({'motivo': 'Debe especificar el motivo de la solicitud de corrección.'})
        updated_case = CaseService.moderate_case(
            case=case,
            actor=request.user,
            estado_publicacion='solicitar_correccion',
            motivo=motivo,
            solicitar_correccion=True,
            request=request,
        )
        corr = updated_case.active_correction_request or updated_case.solicitudes_correccion.first()
        return Response(
            {
                'id_solicitud': str(corr.id) if corr else None,
                'motivo': corr.motivo if corr else motivo,
                'estado': corr.estado if corr else 'pendiente',
                'caso': AdminCaseDetailSerializer(updated_case, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def _handle_assign(self, request):
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
            motivo=serializer.validated_data.get('motivo', ''),
            request=request,
        )
        case.refresh_from_db()
        return Response(AdminCaseDetailSerializer(case, context={'request': request}).data)

    @extend_schema(
        request=CaseAssignResponsibleSerializer,
        responses={200: AdminCaseDetailSerializer},
        summary='Asignar o reasignar responsable territorial al caso (ADM-08)',
    )
    @action(detail=True, methods=['post'], url_path='assignments', permission_classes=[IsAdminOrSuperAdmin])
    def assignments(self, request, pk=None):
        """ADM-08: POST /api/v1/admin/cases/{case_id}/assignments/"""
        return self._handle_assign(request)

    @extend_schema(
        request=CaseAssignResponsibleSerializer,
        responses={200: AdminCaseDetailSerializer},
        summary='Alias compatible para asignar responsable al caso (ADM-08)',
    )
    @action(detail=True, methods=['post'], url_path='assign', permission_classes=[IsAdminOrSuperAdmin])
    def assign(self, request, pk=None):
        """Alias compatible con POST /api/v1/admin/cases/{case_id}/assign/"""
        return self._handle_assign(request)

    def _handle_resolution_or_status(self, request):
        case = self.get_object()
        serializer = CaseManagementStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_case = CaseService.change_management_status(
            case=case,
            actor=request.user,
            new_status_name=serializer.validated_data['resolved_status'],
            motivo=serializer.validated_data['resolved_motivo'],
            resultado_resumen=serializer.validated_data['resolved_resultado'],
            request=request,
        )
        return Response(AdminCaseDetailSerializer(updated_case, context={'request': request}).data)

    @extend_schema(
        request=CaseManagementStatusSerializer,
        responses={200: AdminCaseDetailSerializer},
        summary='Resolver o cerrar narrativamente un caso y cambiar estado operativo (ADM-10)',
    )
    @action(detail=True, methods=['post'], url_path='resolution')
    def resolution(self, request, pk=None):
        """ADM-10 (AMP-11): POST /api/v1/admin/cases/{case_id}/resolution/"""
        return self._handle_resolution_or_status(request)

    @extend_schema(
        request=CaseManagementStatusSerializer,
        responses={200: AdminCaseDetailSerializer},
        summary='Alias compatible para resolver o cerrar un caso (ADM-10)',
    )
    @action(detail=True, methods=['post'], url_path='resolve')
    def resolve(self, request, pk=None):
        """Alias compatible con POST /api/v1/admin/cases/{case_id}/resolve/"""
        return self._handle_resolution_or_status(request)

    @extend_schema(
        request=CaseManagementStatusSerializer,
        responses={200: AdminCaseDetailSerializer},
        summary='Cambiar estado operativo de un caso (ADM-10)',
    )
    @action(detail=True, methods=['post'], url_path='status')
    def change_status(self, request, pk=None):
        """Alias compatible con POST /api/v1/admin/cases/{case_id}/status/"""
        return self._handle_resolution_or_status(request)

    def _handle_progress(self, request):
        case = self.get_object()
        serializer = CaseUpdateCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        seguimiento = CaseService.add_case_update(
            case=case,
            author=request.user,
            titulo=serializer.validated_data['resolved_titulo'],
            descripcion=serializer.validated_data['resolved_descripcion'],
            audiencia=serializer.validated_data['resolved_audiencia'],
            tipo_evento=serializer.validated_data.get('tipo_evento', CaseUpdate.TipoEvento.SEGUIMIENTO),
            visible_publicamente=serializer.validated_data['resolved_visible'],
            new_status=serializer.validated_data['resolved_new_status'],
            files=serializer.validated_data.get('resolved_files'),
            evidence_ids=serializer.validated_data.get('evidence_ids'),
            evidence_description=serializer.validated_data.get('evidence_description'),
            evidence_audiencia=serializer.validated_data.get('evidence_audiencia'),
            request=request,
        )
        return Response(CaseUpdateSerializer(seguimiento, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=CaseUpdateCreateSerializer,
        responses={201: CaseUpdateSerializer},
        summary='Registrar avance o seguimiento con nivel de audiencia y evidencias adjuntas (ADM-09, P24)',
    )
    @action(detail=True, methods=['post'], url_path='progress', parser_classes=[MultiPartParser, FormParser, JSONParser])
    def progress(self, request, pk=None):
        """ADM-09 (AMP-08, P24): POST /api/v1/admin/cases/{case_id}/progress/"""
        return self._handle_progress(request)

    @extend_schema(
        request=CaseUpdateCreateSerializer,
        responses={201: CaseUpdateSerializer},
        summary='Alias compatible para registrar avance o seguimiento con evidencias (ADM-09, P24)',
    )
    @action(detail=True, methods=['post'], url_path='updates', parser_classes=[MultiPartParser, FormParser, JSONParser])
    def add_update(self, request, pk=None):
        """Alias compatible con POST /api/v1/admin/cases/{case_id}/updates/"""
        return self._handle_progress(request)


class AdminCaseEvidenceViewSet(viewsets.ModelViewSet):
    queryset = CaseEvidence.objects.select_related('caso', 'usuario', 'seguimiento').all()
    serializer_class = CaseEvidenceSerializer
    permission_classes = [IsModeratorOrAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        if caso_id := params.get('caso') or params.get('id_caso'):
            qs = qs.filter(caso_id=caso_id)
        if seg_id := params.get('seguimiento') or params.get('id_seguimiento'):
            qs = qs.filter(seguimiento_id=seg_id)
        return qs


class AdminCaseReportView(APIView):
    """
    REP-01: GET /api/v1/admin/reports/cases/
    Retorna agregados de toda la selección autorizada y filas paginadas.
    """
    permission_classes = [IsResponsibleOrAdmin]

    @extend_schema(
        parameters=[
            OpenApiParameter('estado_publicacion', OpenApiTypes.STR, description='pendiente, aprobado, rechazado'),
            OpenApiParameter('id_estado', OpenApiTypes.UUID, description='UUID de estado operativo'),
            OpenApiParameter('estado', OpenApiTypes.STR, description='Nombre de estado operativo'),
            OpenApiParameter('prioridad', OpenApiTypes.STR, description='baja, media, alta, critica'),
            OpenApiParameter('id_departamento', OpenApiTypes.UUID, description='UUID de departamento'),
            OpenApiParameter('id_municipio', OpenApiTypes.UUID, description='UUID de municipio'),
            OpenApiParameter('id_comunidad', OpenApiTypes.UUID, description='UUID de comunidad'),
            OpenApiParameter('id_tipo_caso', OpenApiTypes.UUID, description='UUID de tipo de caso'),
            OpenApiParameter('categoria', OpenApiTypes.STR, description='Categoría temática textual'),
            OpenApiParameter('naturaleza', OpenApiTypes.STR, description='problematica, proyecto_iniciativa, otro'),
            OpenApiParameter('id_responsable', OpenApiTypes.UUID, description='UUID de responsable activo'),
            OpenApiParameter('search', OpenApiTypes.STR, description='Búsqueda por código, título o descripción'),
            OpenApiParameter('page', OpenApiTypes.INT, description='Número de página (1..N)'),
            OpenApiParameter('page_size', OpenApiTypes.INT, description='Tamaño de página (default 20)'),
        ],
        responses={
            200: inline_serializer(
                name='AdminCaseReportResponse',
                fields={
                    'kpis': drf_serializers.DictField(),
                    'totals': drf_serializers.DictField(),
                    'count': drf_serializers.IntegerField(),
                    'page': drf_serializers.IntegerField(),
                    'page_size': drf_serializers.IntegerField(),
                    'results': AdminCaseDetailSerializer(many=True),
                },
            )
        },
        summary='Informe filtrado de casos con agregados globales y filas paginadas (REP-01)',
    )
    def get(self, request):
        qs = (
            Case.objects.select_related(
                'usuario',
                'tipo_caso',
                'comunidad',
                'comunidad__municipio',
                'comunidad__municipio__departamento',
                'estado',
            )
            .prefetch_related('asignaciones__responsable')
            .all()
        )
        if not request.user.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR):
            qs = qs.filter(asignaciones__responsable=request.user, asignaciones__activo=True).distinct()

        qs = apply_admin_case_filters(qs, request.query_params)

        totals = {
            'total_cases': qs.count(),
            'by_estado': dict(qs.values_list('estado__nombre').annotate(total=Count('id'))),
            'by_estado_publicacion': dict(qs.values_list('estado_publicacion').annotate(total=Count('id'))),
            'by_prioridad': dict(qs.values_list('prioridad').annotate(total=Count('id'))),
            'by_categoria': dict(qs.values_list('tipo_caso__categoria').annotate(total=Count('id'))),
            'by_municipio': dict(qs.values_list('comunidad__municipio__nombre').annotate(total=Count('id'))),
        }

        try:
            page_size = max(min(int(request.query_params.get('page_size', 20)), 100), 1)
            page = max(int(request.query_params.get('page', 1)), 1)
        except (ValueError, TypeError):
            return Response(
                {
                    'code': 'invalid_parameter',
                    'message': 'Los parámetros page y page_size deben ser números enteros positivos.',
                    'errors': {'page': ['Debe ser un entero positivo.'], 'page_size': ['Debe ser un entero entre 1 y 100.']},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        start = (page - 1) * page_size
        end = start + page_size

        return Response({
            'kpis': totals,
            'totals': totals,
            'count': totals['total_cases'],
            'page': page,
            'page_size': page_size,
            'results': AdminCaseDetailSerializer(qs[start:end], many=True, context={'request': request}).data,
        })


def _sanitize_csv_cell(val) -> str:
    if val is None:
        return ''
    text = str(val)
    if text.startswith(('=', '+', '-', '@')):
        return f"'{text}"
    return text


class AdminCaseReportExportCSVView(APIView):
    """
    REP-02: GET /api/v1/admin/reports/cases/export/
    Exporta en CSV toda la selección autorizada neutralizando fórmulas en celdas de texto.
    """
    permission_classes = [IsResponsibleOrAdmin]

    @extend_schema(
        parameters=[
            OpenApiParameter('estado_publicacion', OpenApiTypes.STR),
            OpenApiParameter('id_estado', OpenApiTypes.UUID),
            OpenApiParameter('estado', OpenApiTypes.STR),
            OpenApiParameter('prioridad', OpenApiTypes.STR),
            OpenApiParameter('id_departamento', OpenApiTypes.UUID),
            OpenApiParameter('id_municipio', OpenApiTypes.UUID),
            OpenApiParameter('id_comunidad', OpenApiTypes.UUID),
            OpenApiParameter('id_tipo_caso', OpenApiTypes.UUID),
            OpenApiParameter('categoria', OpenApiTypes.STR),
            OpenApiParameter('naturaleza', OpenApiTypes.STR),
            OpenApiParameter('id_responsable', OpenApiTypes.UUID),
            OpenApiParameter('search', OpenApiTypes.STR),
        ],
        responses={(200, 'text/csv'): OpenApiTypes.BINARY},
        summary='Exportación CSV de toda la selección filtrada de casos (REP-02)',
    )
    def get(self, request):
        qs = (
            Case.objects.select_related(
                'tipo_caso',
                'comunidad',
                'comunidad__municipio',
                'comunidad__municipio__departamento',
                'estado',
            )
            .prefetch_related('asignaciones__responsable')
            .all()
        )
        if not request.user.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR):
            qs = qs.filter(asignaciones__responsable=request.user, asignaciones__activo=True).distinct()

        qs = apply_admin_case_filters(qs, request.query_params)

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="informe_casos_plus.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'id_caso',
            'codigo',
            'titulo',
            'tipo_caso',
            'categoria',
            'naturaleza',
            'estado_operativo',
            'estado_publicacion',
            'prioridad',
            'departamento',
            'municipio',
            'comunidad',
            'responsable_activo',
            'familias_afectadas',
            'meses_afectacion',
            'fecha_creacion',
            'fecha_aprobacion',
            'fecha_resolucion',
        ])

        for c in qs:
            active_assign = c.active_assignment
            writer.writerow([
                str(c.id),
                _sanitize_csv_cell(c.codigo),
                _sanitize_csv_cell(c.titulo),
                _sanitize_csv_cell(c.tipo_caso.nombre),
                _sanitize_csv_cell(c.tipo_caso.categoria),
                _sanitize_csv_cell(c.tipo_caso.naturaleza),
                _sanitize_csv_cell(c.estado.nombre),
                _sanitize_csv_cell(c.estado_publicacion),
                _sanitize_csv_cell(c.prioridad),
                _sanitize_csv_cell(c.comunidad.municipio.departamento.nombre),
                _sanitize_csv_cell(c.comunidad.municipio.nombre),
                _sanitize_csv_cell(c.comunidad.nombre),
                _sanitize_csv_cell(active_assign.responsable.full_name if active_assign else ''),
                c.familias_afectadas if c.familias_afectadas is not None else '',
                c.meses_afectacion if c.meses_afectacion is not None else '',
                c.fecha_creacion.isoformat() if c.fecha_creacion else '',
                c.fecha_aprobacion.isoformat() if c.fecha_aprobacion else '',
                c.fecha_resolucion.isoformat() if c.fecha_resolucion else '',
            ])
        return response
