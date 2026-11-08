from rest_framework import generics, permissions, viewsets
from apps.accounts.permissions import IsAdminOrSuperAdmin
from apps.audit.services import AuditService
from apps.territories.models import Community, Department, Municipality
from apps.territories.serializers import (
    CommunitySerializer,
    DepartmentSerializer,
    MunicipalitySerializer,
)


class AuditedTerritoryViewSetMixin:
    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        instance = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='territorios',
            target_model=instance._meta.db_table,
            target_id=instance.pk,
            description=f'Creación de territorio: {instance}',
            new_data=serializer.data,
            request=self.request,
        )

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        instance = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='update',
            module='territorios',
            target_model=instance._meta.db_table,
            target_id=instance.pk,
            description=f'Actualización de territorio: {instance}',
            new_data=serializer.data,
            request=self.request,
        )

    def perform_destroy(self, instance):
        AuditService.set_db_actor_session(self.request.user)
        target_id = instance.pk
        table_name = instance._meta.db_table
        name = str(instance)
        instance.delete()
        AuditService.log(
            actor=self.request.user,
            action='delete',
            module='territorios',
            target_model=table_name,
            target_id=target_id,
            description=f'Eliminación de territorio: {name}',
            request=self.request,
        )


class AdminDepartmentViewSet(AuditedTerritoryViewSetMixin, viewsets.ModelViewSet):
    queryset = Department.objects.prefetch_related('municipios').all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrSuperAdmin]


class AdminMunicipalityViewSet(AuditedTerritoryViewSetMixin, viewsets.ModelViewSet):
    serializer_class = MunicipalitySerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        qs = Municipality.objects.select_related('departamento').all()
        if dept := (self.request.query_params.get('departamento') or self.request.query_params.get('department')):
            qs = qs.filter(departamento_id=dept)
        return qs


class AdminCommunityViewSet(AuditedTerritoryViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CommunitySerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        qs = Community.objects.select_related('municipio', 'municipio__departamento').all()
        params = self.request.query_params
        if muni := (params.get('municipio') or params.get('municipality')):
            qs = qs.filter(municipio_id=muni)
        if tipo := (params.get('tipo') or params.get('community_type')):
            qs = qs.filter(tipo=tipo.lower())
        if activo := (params.get('activo') or params.get('is_active')):
            qs = qs.filter(activo=activo.lower() == 'true')
        return qs


class PublicDepartmentListView(generics.ListAPIView):
    queryset = Department.objects.prefetch_related('municipios').all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class PublicMunicipalityListView(generics.ListAPIView):
    serializer_class = MunicipalitySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = Municipality.objects.select_related('departamento').all()
        if dept := (self.request.query_params.get('departamento') or self.request.query_params.get('department')):
            qs = qs.filter(departamento_id=dept)
        return qs


class PublicCommunityListView(generics.ListAPIView):
    serializer_class = CommunitySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = Community.objects.filter(activo=True).select_related('municipio')
        muni_id = (
            self.kwargs.get('municipality_id')
            or self.request.query_params.get('municipio')
            or self.request.query_params.get('municipality')
        )
        if muni_id:
            qs = qs.filter(municipio_id=muni_id)
        return qs
