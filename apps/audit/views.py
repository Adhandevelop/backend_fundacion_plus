from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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
