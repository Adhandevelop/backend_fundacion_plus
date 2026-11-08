from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from apps.accounts.permissions import IsEditorOrAdmin
from apps.audit.services import AuditService
from apps.initiatives.models import (
    Initiative,
    InitiativeActivity,
    InitiativeEdition,
    InitiativeMedia,
    InitiativeMetric,
)
from apps.initiatives.serializers import (
    AdminInitiativeSerializer,
    InitiativeActivitySerializer,
    InitiativeDetailSerializer,
    InitiativeEditionSerializer,
    InitiativeListSerializer,
    InitiativeMediaSerializer,
    InitiativeMetricSerializer,
)


class PublicInitiativeListView(generics.ListAPIView):
    serializer_class = InitiativeListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Initiative.objects.filter(
            estado_publicacion=Initiative.EstadoPublicacion.PUBLICADA
        ).prefetch_related('multimedia', 'ediciones__indicadores')
        params = self.request.query_params
        if destacada := (params.get('destacada') or params.get('is_featured')):
            qs = qs.filter(destacada=destacada.lower() == 'true')
        if categoria := (params.get('categoria') or params.get('category')):
            qs = qs.filter(categoria__iexact=categoria)
        if search := params.get('search'):
            qs = qs.filter(titulo__icontains=search) | qs.filter(descripcion_corta__icontains=search)
        return qs


class PublicInitiativeDetailView(generics.RetrieveAPIView):
    serializer_class = InitiativeDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        lookup = self.kwargs['lookup']
        qs = Initiative.objects.filter(
            estado_publicacion=Initiative.EstadoPublicacion.PUBLICADA
        ).prefetch_related('ediciones__indicadores', 'ediciones__actividades', 'multimedia')
        obj = qs.filter(slug=lookup).first()
        if not obj:
            obj = get_object_or_404(qs, pk=lookup)
        return obj


class AdminInitiativeViewSet(viewsets.ModelViewSet):
    serializer_class = AdminInitiativeSerializer
    permission_classes = [IsEditorOrAdmin]

    def get_queryset(self):
        qs = Initiative.objects.prefetch_related('ediciones', 'multimedia').all()
        params = self.request.query_params
        if pub := (params.get('estado_publicacion') or params.get('publication_status')):
            qs = qs.filter(estado_publicacion__iexact=pub)
        if destacada := (params.get('destacada') or params.get('is_featured')):
            qs = qs.filter(destacada=destacada.lower() == 'true')
        return qs

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        instance = serializer.save(creador=self.request.user)
        instance.get_or_create_current_edition()
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='iniciativas',
            target_model='iniciativas',
            target_id=instance.pk,
            description=f'Creación de iniciativa: {instance.titulo}',
            request=self.request,
        )

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        instance = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='update',
            module='iniciativas',
            target_model='iniciativas',
            target_id=instance.pk,
            description=f'Actualización de iniciativa: {instance.titulo} ({instance.estado_publicacion})',
            request=self.request,
        )


class AdminInitiativeEditionViewSet(viewsets.ModelViewSet):
    queryset = InitiativeEdition.objects.select_related('iniciativa').all()
    serializer_class = InitiativeEditionSerializer
    permission_classes = [IsEditorOrAdmin]

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        serializer.save()


class AdminInitiativeActivityViewSet(viewsets.ModelViewSet):
    queryset = InitiativeActivity.objects.select_related('edicion', 'comunidad', 'responsable').all()
    serializer_class = InitiativeActivitySerializer
    permission_classes = [IsEditorOrAdmin]

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        serializer.save()


class AdminInitiativeMediaViewSet(viewsets.ModelViewSet):
    queryset = InitiativeMedia.objects.select_related('iniciativa', 'edicion').all()
    serializer_class = InitiativeMediaSerializer
    permission_classes = [IsEditorOrAdmin]


class AdminInitiativeMetricViewSet(viewsets.ModelViewSet):
    queryset = InitiativeMetric.objects.select_related('edicion').all()
    serializer_class = InitiativeMetricSerializer
    permission_classes = [IsEditorOrAdmin]
