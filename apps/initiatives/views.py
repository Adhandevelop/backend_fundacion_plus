import uuid as uuid_lib
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsEditorOrAdmin
from apps.audit.services import AuditService
from apps.initiatives.models import (
    Initiative,
    InitiativeActivity,
    InitiativeCaseLink,
    InitiativeCommunity,
    InitiativeEdition,
    InitiativeMedia,
    InitiativeMetric,
)
from apps.initiatives.serializers import (
    AdminInitiativeSerializer,
    InitiativeActivitySerializer,
    InitiativeCaseLinkSerializer,
    InitiativeCommunitySerializer,
    InitiativeDetailSerializer,
    InitiativeEditionSerializer,
    InitiativeListSerializer,
    InitiativeMediaSerializer,
    InitiativeMetricSerializer,
)


def resolve_published_initiative(lookup: str) -> Initiative:
    qs = Initiative.objects.filter(
        estado_publicacion=Initiative.EstadoPublicacion.PUBLICADA
    ).prefetch_related('ediciones__indicadores', 'ediciones__actividades', 'multimedia')
    by_slug = qs.filter(slug=lookup).first()
    if by_slug:
        return by_slug
    try:
        uuid_val = uuid_lib.UUID(str(lookup).strip())
        return get_object_or_404(qs, pk=uuid_val)
    except (ValueError, TypeError):
        return get_object_or_404(qs, slug=lookup)


class PublicInitiativeCategoryListView(APIView):
    """
    CAT-08: GET /api/v1/catalogs/initiative-categories/
    Retorna valores distintos de `iniciativas.categoria` para programas publicados.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cats = list(
            dict.fromkeys(
                Initiative.objects.filter(estado_publicacion=Initiative.EstadoPublicacion.PUBLICADA)
                .order_by('categoria')
                .values_list('categoria', flat=True)
            )
        )
        return Response({'categories': cats})


class PublicInitiativeListView(generics.ListAPIView):
    """PUB-05: GET /api/v1/public/initiatives/"""
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
        if anio := params.get('anio'):
            qs = qs.filter(ediciones__anio=anio).distinct()
        if search := params.get('search'):
            qs = qs.filter(Q(titulo__icontains=search) | Q(descripcion_corta__icontains=search))
        return qs


class PublicInitiativeDetailView(generics.RetrieveAPIView):
    """PUB-06: GET /api/v1/public/initiatives/{slug}/"""
    serializer_class = InitiativeDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return resolve_published_initiative(self.kwargs['lookup'])


class PublicInitiativeGalleryView(generics.ListAPIView):
    """PUB-07: GET /api/v1/public/initiatives/{id}/gallery/"""
    serializer_class = InitiativeMediaSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        from apps.initiatives.models import InitiativeMedia

        lookup = self.kwargs.get('lookup') or self.request.query_params.get('id_iniciativa')
        if lookup:
            initiative = resolve_published_initiative(lookup)
            qs = initiative.multimedia.all()
        else:
            qs = InitiativeMedia.objects.filter(
                iniciativa__estado_publicacion=Initiative.EstadoPublicacion.PUBLICADA
            )
        if edicion_id := self.request.query_params.get('id_edicion'):
            if edicion_id.lower() in ('null', 'general'):
                qs = qs.filter(edicion__isnull=True)
            else:
                qs = qs.filter(edicion_id=edicion_id)
        return qs


class PublicInitiativeEditionListView(generics.ListAPIView):
    """INI-01: GET /api/v1/public/initiatives/{id}/editions/"""
    serializer_class = InitiativeEditionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        initiative = resolve_published_initiative(self.kwargs['lookup'])
        qs = initiative.ediciones.prefetch_related('indicadores', 'actividades', 'comunidades_vinculadas').all()
        if anio := self.request.query_params.get('anio'):
            qs = qs.filter(anio=anio)
        return qs


class PublicInitiativeEditionDetailView(generics.RetrieveAPIView):
    """
    INI-02: GET /api/v1/public/initiatives/{id}/editions/{edition_id}/
    Comprueba estrictamente la pertenencia de la edición al programa indicado.
    """
    serializer_class = InitiativeEditionSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        initiative = resolve_published_initiative(self.kwargs['lookup'])
        return get_object_or_404(
            initiative.ediciones.prefetch_related('indicadores', 'actividades', 'comunidades_vinculadas'),
            pk=self.kwargs['edition_id'],
        )


class PublicInitiativeEditionActivityListView(generics.ListAPIView):
    """
    INI-03: GET /api/v1/public/initiatives/{id}/editions/{edition_id}/activities/
    """
    serializer_class = InitiativeActivitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        initiative = resolve_published_initiative(self.kwargs['lookup'])
        edition = get_object_or_404(initiative.ediciones.all(), pk=self.kwargs['edition_id'])
        return edition.actividades.select_related('comunidad', 'responsable').all()


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

    def get_queryset(self):
        qs = super().get_queryset()
        if init_id := self.request.query_params.get('id_iniciativa'):
            qs = qs.filter(iniciativa_id=init_id)
        return qs

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


class AdminInitiativeCommunityViewSet(viewsets.ModelViewSet):
    queryset = InitiativeCommunity.objects.select_related('edicion', 'comunidad').all()
    serializer_class = InitiativeCommunitySerializer
    permission_classes = [IsEditorOrAdmin]


class AdminInitiativeCaseLinkViewSet(viewsets.ModelViewSet):
    queryset = InitiativeCaseLink.objects.select_related('edicion', 'caso').all()
    serializer_class = InitiativeCaseLinkSerializer
    permission_classes = [IsEditorOrAdmin]
