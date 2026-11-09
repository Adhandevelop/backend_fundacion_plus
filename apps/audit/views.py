from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, inline_serializer
from rest_framework import mixins, serializers as drf_serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.permissions import IsAdminOrSuperAdmin
from apps.audit.models import (
    AuditAccess,
    AuditCase,
    AuditLog,
    AuditPermission,
    AuditSecurity,
)
from apps.audit.serializers import (
    AuditAccessSerializer,
    AuditCaseSerializer,
    AuditLogSerializer,
    AuditPermissionSerializer,
    AuditSecuritySerializer,
)


class AdminAuditLogViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Endpoint administrativo de solo lectura para consultar las 5 tablas de auditoría de `plus`:
    - GET /api/v1/admin/audit-logs/ (auditoria_eventos)
    - GET /api/v1/admin/audit-logs/accesos/ (auditoria_accesos)
    - GET /api/v1/admin/audit-logs/casos/ (auditoria_casos)
    - GET /api/v1/admin/audit-logs/permisos/ (auditoria_permisos)
    - GET /api/v1/admin/audit-logs/seguridad/ (auditoria_seguridad)
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        qs = AuditLog.objects.select_related('usuario').all()
        params = self.request.query_params
        if modulo := (params.get('modulo') or params.get('module')):
            qs = qs.filter(modulo__iexact=modulo)
        if accion := (params.get('accion') or params.get('action')):
            qs = qs.filter(accion__iexact=accion)
        if tabla := params.get('tabla_afectada'):
            qs = qs.filter(tabla_afectada__iexact=tabla)
        if usuario := (params.get('usuario') or params.get('actor')):
            qs = qs.filter(usuario_id=usuario)
        return qs

    @action(detail=False, methods=['get'], url_path='accesos')
    def accesos(self, request):
        qs = AuditAccess.objects.select_related('usuario').all()[:200]
        return Response(AuditAccessSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='casos')
    def casos(self, request):
        qs = AuditCase.objects.select_related('caso', 'usuario').all()[:200]
        return Response(AuditCaseSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='permisos')
    def permisos(self, request):
        qs = AuditPermission.objects.select_related('usuario_afectado', 'usuario_responsable').all()[:200]
        return Response(AuditPermissionSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='seguridad')
    def seguridad(self, request):
        qs = AuditSecurity.objects.select_related('usuario').all()[:200]
        return Response(AuditSecuritySerializer(qs, many=True).data)


class AdminAuditEventListView(APIView):
    """
    AUD-01: GET /api/v1/admin/audit-events/ (y /api/v1/admin/audit/events/)
    Proyección unificada de las 5 tablas de auditoría con referencia `event_ref` (`{source}:{uuid}`).
    """
    permission_classes = [IsAdminOrSuperAdmin]

    @extend_schema(
        parameters=[
            OpenApiParameter('source', OpenApiTypes.STR, description='Fuente: eventos, accesos, casos, permisos, seguridad'),
            OpenApiParameter('actor', OpenApiTypes.UUID, description='Filtrar por UUID de usuario actor'),
            OpenApiParameter('action', OpenApiTypes.STR, description='Filtrar por tipo de acción'),
        ],
        responses={
            200: inline_serializer(
                name='AdminAuditEventListResponse',
                fields={
                    'kpis': drf_serializers.DictField(),
                    'count': drf_serializers.IntegerField(),
                    'results': drf_serializers.ListField(
                        child=inline_serializer(
                            name='UnifiedAuditEventItem',
                            fields={
                                'event_ref': drf_serializers.CharField(),
                                'id': drf_serializers.UUIDField(),
                                'source': drf_serializers.CharField(),
                                'action': drf_serializers.CharField(),
                                'module': drf_serializers.CharField(),
                                'entity': drf_serializers.CharField(allow_null=True),
                                'entity_id': drf_serializers.CharField(allow_null=True),
                                'actor': drf_serializers.UUIDField(allow_null=True),
                                'actor_nombre': drf_serializers.CharField(allow_null=True),
                                'result': drf_serializers.CharField(),
                                'description': drf_serializers.CharField(allow_null=True),
                                'changed_columns': drf_serializers.ListField(
                                    child=drf_serializers.CharField(), allow_null=True
                                ),
                                'timestamp': drf_serializers.DateTimeField(),
                            },
                        )
                    ),
                },
            )
        },
        summary='Listado unificado de las 5 fuentes de auditoría con KPIs y filtros (AUD-01)',
    )
    def get(self, request):
        params = request.query_params
        source_filter = (params.get('source') or params.get('fuente') or '').strip().lower()
        actor_filter = params.get('actor') or params.get('id_usuario')
        action_filter = params.get('action') or params.get('accion')

        items = []

        if not source_filter or source_filter in ('eventos', 'auditoria_eventos'):
            qs = AuditLog.objects.select_related('usuario').all()
            if actor_filter:
                qs = qs.filter(usuario_id=actor_filter)
            if action_filter:
                qs = qs.filter(accion__iexact=action_filter)
            for e in qs[:100]:
                changed_cols = None
                desc = f'{e.accion} en {e.tabla_afectada or e.modulo}'
                if isinstance(e.datos_nuevos, dict):
                    changed_cols = e.datos_nuevos.get('columnas_modificadas')
                    desc = e.datos_nuevos.get('_descripcion') or desc
                items.append({
                    'event_ref': f'eventos:{e.id}',
                    'id': str(e.id),
                    'source': 'auditoria_eventos',
                    'action': e.accion,
                    'module': e.modulo,
                    'entity': e.tabla_afectada,
                    'entity_id': str(e.id_registro) if e.id_registro else None,
                    'actor': str(e.usuario_id) if e.usuario_id else None,
                    'actor_nombre': e.usuario.full_name if e.usuario else None,
                    'result': e.resultado,
                    'description': desc,
                    'changed_columns': changed_cols,
                    'timestamp': e.fecha_evento,
                })

        if not source_filter or source_filter in ('accesos', 'auditoria_accesos'):
            qs = AuditAccess.objects.select_related('usuario').all()
            if actor_filter:
                qs = qs.filter(usuario_id=actor_filter)
            for a in qs[:100]:
                items.append({
                    'event_ref': f'accesos:{a.id}',
                    'id': str(a.id),
                    'source': 'auditoria_accesos',
                    'action': a.tipo_evento,
                    'module': 'autenticacion',
                    'entity': 'usuarios',
                    'entity_id': str(a.usuario_id) if a.usuario_id else None,
                    'actor': str(a.usuario_id) if a.usuario_id else None,
                    'actor_nombre': a.usuario.full_name if a.usuario else None,
                    'result': a.resultado,
                    'description': f'Acceso ({a.tipo_evento}): {a.resultado}',
                    'changed_columns': None,
                    'timestamp': a.fecha_evento,
                })

        if not source_filter or source_filter in ('casos', 'auditoria_casos'):
            qs = AuditCase.objects.select_related('caso', 'usuario').all()
            if actor_filter:
                qs = qs.filter(usuario_id=actor_filter)
            for c in qs[:100]:
                items.append({
                    'event_ref': f'casos:{c.id}',
                    'id': str(c.id),
                    'source': 'auditoria_casos',
                    'action': c.tipo_accion,
                    'module': 'casos',
                    'entity': 'casos',
                    'entity_id': str(c.caso_id),
                    'actor': str(c.usuario_id) if c.usuario_id else None,
                    'actor_nombre': c.usuario.full_name if c.usuario else None,
                    'result': 'exitoso',
                    'description': c.motivo or f'{c.tipo_accion}: {c.estado_anterior} -> {c.estado_nuevo}',
                    'before_after': {'estado_anterior': c.estado_anterior, 'estado_nuevo': c.estado_nuevo},
                    'changed_columns': None,
                    'timestamp': c.fecha_accion,
                })

        if not source_filter or source_filter in ('permisos', 'auditoria_permisos'):
            qs = AuditPermission.objects.select_related('usuario_afectado', 'usuario_responsable').all()
            if actor_filter:
                qs = qs.filter(usuario_responsable_id=actor_filter)
            for p in qs[:100]:
                items.append({
                    'event_ref': f'permisos:{p.id}',
                    'id': str(p.id),
                    'source': 'auditoria_permisos',
                    'action': p.tipo_cambio,
                    'module': 'permisos',
                    'entity': 'usuarios',
                    'entity_id': str(p.usuario_afectado_id),
                    'actor': str(p.usuario_responsable_id) if p.usuario_responsable_id else None,
                    'actor_nombre': p.usuario_responsable.full_name if p.usuario_responsable else None,
                    'result': 'exitoso',
                    'description': p.motivo or f'Cambio de permisos ({p.tipo_cambio})',
                    'before_after': {'valor_anterior': p.valor_anterior, 'valor_nuevo': p.valor_nuevo},
                    'changed_columns': None,
                    'timestamp': p.fecha_cambio,
                })

        if not source_filter or source_filter in ('seguridad', 'auditoria_seguridad'):
            qs = AuditSecurity.objects.select_related('usuario').all()
            for s in qs[:100]:
                items.append({
                    'event_ref': f'seguridad:{s.id}',
                    'id': str(s.id),
                    'source': 'auditoria_seguridad',
                    'action': s.tipo_evento,
                    'module': 'seguridad',
                    'entity': 'seguridad',
                    'entity_id': None,
                    'actor': str(s.usuario_id) if s.usuario_id else None,
                    'actor_nombre': s.usuario.full_name if s.usuario else None,
                    'result': s.nivel_severidad,
                    'description': s.descripcion,
                    'changed_columns': None,
                    'timestamp': s.fecha_evento,
                })

        items.sort(key=lambda x: x['timestamp'], reverse=True)
        return Response({
            'kpis': {
                'total_events': len(items),
                'eventos': AuditLog.objects.count(),
                'accesos': AuditAccess.objects.count(),
                'casos': AuditCase.objects.count(),
                'permisos': AuditPermission.objects.count(),
                'seguridad': AuditSecurity.objects.count(),
            },
            'count': len(items),
            'results': items[:200],
        })


class AdminAuditEventDetailView(APIView):
    """
    AUD-02: GET /api/v1/admin/audit/events/{event_ref}/
    Soporta referencia `{source}:{uuid}` o búsqueda directa por UUID.
    """
    permission_classes = [IsAdminOrSuperAdmin]

    @extend_schema(
        responses={200: AuditLogSerializer},
        summary='Detalle de evento de auditoría por referencia {source}:{uuid} o UUID (AUD-02)',
    )
    def get(self, request, event_ref: str = None, event_id: str = None):
        event_ref = str(event_ref or event_id or '')
        if ':' in event_ref:
            source, pk = event_ref.split(':', 1)
        else:
            source, pk = '', event_ref

        source = source.lower()
        if source in ('eventos', 'auditoria_eventos', ''):
            obj = AuditLog.objects.select_related('usuario').filter(pk=pk).first()
            if obj:
                return Response({
                    'event_ref': f'eventos:{obj.id}',
                    'source': 'auditoria_eventos',
                    **AuditLogSerializer(obj).data,
                })
        if source in ('accesos', 'auditoria_accesos', ''):
            obj = AuditAccess.objects.select_related('usuario').filter(pk=pk).first()
            if obj:
                return Response({
                    'event_ref': f'accesos:{obj.id}',
                    'source': 'auditoria_accesos',
                    **AuditAccessSerializer(obj).data,
                })
        if source in ('casos', 'auditoria_casos', ''):
            obj = AuditCase.objects.select_related('caso', 'usuario').filter(pk=pk).first()
            if obj:
                return Response({
                    'event_ref': f'casos:{obj.id}',
                    'source': 'auditoria_casos',
                    **AuditCaseSerializer(obj).data,
                })
        if source in ('permisos', 'auditoria_permisos', ''):
            obj = AuditPermission.objects.select_related('usuario_afectado', 'usuario_responsable').filter(pk=pk).first()
            if obj:
                return Response({
                    'event_ref': f'permisos:{obj.id}',
                    'source': 'auditoria_permisos',
                    **AuditPermissionSerializer(obj).data,
                })
        if source in ('seguridad', 'auditoria_seguridad', ''):
            obj = AuditSecurity.objects.select_related('usuario').filter(pk=pk).first()
            if obj:
                return Response({
                    'event_ref': f'seguridad:{obj.id}',
                    'source': 'auditoria_seguridad',
                    **AuditSecuritySerializer(obj).data,
                })

        obj = get_object_or_404(AuditLog, pk=pk)
        return Response(AuditLogSerializer(obj).data)
