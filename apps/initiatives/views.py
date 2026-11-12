import uuid as uuid_lib
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, permissions, serializers as drf_serializers, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
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
    PublicInitiativeActivitySerializer,
    PublicInitiativeEditionSerializer,
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

    @extend_schema(
        responses={
            200: inline_serializer(
                name='PublicInitiativeCategoriesResponse',
                fields={
                    'categories': drf_serializers.ListField(child=drf_serializers.CharField()),
                },
            )
        },
        summary='Categorías distintas de iniciativas publicadas (CAT-08)',
    )
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
    serializer_class = PublicInitiativeEditionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        initiative = resolve_published_initiative(self.kwargs['lookup'])
        qs = initiative.ediciones.prefetch_related('indicadores', 'actividades').all()
        if anio := self.request.query_params.get('anio'):
            qs = qs.filter(anio=anio)
        return qs


class PublicInitiativeEditionDetailView(generics.RetrieveAPIView):
    """
    INI-02: GET /api/v1/public/initiatives/{id}/editions/{edition_id}/
    Comprueba estrictamente la pertenencia de la edición al programa indicado.
    """
    serializer_class = PublicInitiativeEditionSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        initiative = resolve_published_initiative(self.kwargs['lookup'])
        return get_object_or_404(
            initiative.ediciones.prefetch_related('indicadores', 'actividades'),
            pk=self.kwargs['edition_id'],
        )


class PublicInitiativeEditionActivityListView(generics.ListAPIView):
    """
    INI-03: GET /api/v1/public/initiatives/{id}/editions/{edition_id}/activities/
    """
    serializer_class = PublicInitiativeActivitySerializer
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
        prev_status = serializer.instance.estado_publicacion
        instance = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='update',
            module='iniciativas',
            target_model='iniciativas',
            target_id=instance.pk,
            description=f'Actualización de iniciativa: {instance.titulo} ({prev_status} -> {instance.estado_publicacion})',
            previous_data={'estado_publicacion': prev_status},
            new_data={'estado_publicacion': instance.estado_publicacion},
            request=self.request,
        )

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        """P20: Publicación formal de iniciativa con auditoría."""
        initiative = self.get_object()
        AuditService.set_db_actor_session(request.user)
        prev_status = initiative.estado_publicacion
        initiative.estado_publicacion = Initiative.EstadoPublicacion.PUBLICADA
        if not initiative.fecha_publicacion:
            initiative.fecha_publicacion = timezone.now()
        initiative.save(update_fields=['estado_publicacion', 'fecha_publicacion', 'fecha_actualizacion'])
        AuditService.log(
            actor=request.user,
            action='publish',
            module='iniciativas',
            target_model='iniciativas',
            target_id=initiative.pk,
            description=f'Publicación de iniciativa: {initiative.titulo}',
            previous_data={'estado_publicacion': prev_status},
            new_data={'estado_publicacion': initiative.estado_publicacion},
            request=request,
        )
        return Response(AdminInitiativeSerializer(initiative).data)

    @action(detail=True, methods=['post'], url_path='archive')
    def archive(self, request, pk=None):
        """P20: Finalizado/archivado operativo de iniciativa con auditoría."""
        initiative = self.get_object()
        AuditService.set_db_actor_session(request.user)
        prev_estado = initiative.estado
        initiative.estado = Initiative.Estado.FINALIZADA
        initiative.save(update_fields=['estado', 'fecha_actualizacion'])
        AuditService.log(
            actor=request.user,
            action='archive',
            module='iniciativas',
            target_model='iniciativas',
            target_id=initiative.pk,
            description=f'Archivado de iniciativa: {initiative.titulo}',
            previous_data={'estado': prev_estado},
            new_data={'estado': initiative.estado},
            request=request,
        )
        return Response(AdminInitiativeSerializer(initiative).data)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """P20: Rechazo formal de iniciativa con auditoría."""
        initiative = self.get_object()
        AuditService.set_db_actor_session(request.user)
        prev_status = initiative.estado_publicacion
        initiative.estado_publicacion = Initiative.EstadoPublicacion.RECHAZADA
        initiative.save(update_fields=['estado_publicacion', 'fecha_actualizacion'])
        AuditService.log(
            actor=request.user,
            action='reject',
            module='iniciativas',
            target_model='iniciativas',
            target_id=initiative.pk,
            description=f'Rechazo de publicación de iniciativa: {initiative.titulo}',
            previous_data={'estado_publicacion': prev_status},
            new_data={'estado_publicacion': initiative.estado_publicacion},
            request=request,
        )
        return Response(AdminInitiativeSerializer(initiative).data)


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
        edition = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='iniciativas',
            target_model='iniciativa_ediciones',
            target_id=edition.pk,
            description=f'Creación de edición "{edition.nombre_edicion}" ({edition.anio}) para iniciativa {edition.iniciativa_id}',
            request=self.request,
        )

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        edition = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='update',
            module='iniciativas',
            target_model='iniciativa_ediciones',
            target_id=edition.pk,
            description=f'Actualización de edición "{edition.nombre_edicion}" ({edition.anio})',
            request=self.request,
        )

    def perform_destroy(self, instance):
        AuditService.set_db_actor_session(self.request.user)
        ed_id = instance.pk
        ini_id = instance.iniciativa_id
        instance.delete()
        AuditService.log(
            actor=self.request.user,
            action='delete',
            module='iniciativas',
            target_model='iniciativa_ediciones',
            target_id=ed_id,
            description=f'Eliminación de edición {ed_id} en iniciativa {ini_id}',
            request=self.request,
        )


class AdminInitiativeActivityViewSet(viewsets.ModelViewSet):
    queryset = InitiativeActivity.objects.select_related('edicion', 'comunidad', 'responsable').all()
    serializer_class = InitiativeActivitySerializer
    permission_classes = [IsEditorOrAdmin]

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        act = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='iniciativas',
            target_model='iniciativa_actividades',
            target_id=act.pk,
            description=f'Creación de actividad "{act.titulo}" en edición {act.edicion_id}',
            request=self.request,
        )

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        act = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='update',
            module='iniciativas',
            target_model='iniciativa_actividades',
            target_id=act.pk,
            description=f'Actualización de actividad "{act.titulo}"',
            request=self.request,
        )

    def perform_destroy(self, instance):
        AuditService.set_db_actor_session(self.request.user)
        act_id = instance.pk
        ed_id = instance.edicion_id
        instance.delete()
        AuditService.log(
            actor=self.request.user,
            action='delete',
            module='iniciativas',
            target_model='iniciativa_actividades',
            target_id=act_id,
            description=f'Eliminación de actividad {act_id} en edición {ed_id}',
            request=self.request,
        )


class AdminInitiativeMediaViewSet(viewsets.ModelViewSet):
    queryset = InitiativeMedia.objects.select_related('iniciativa', 'edicion').all()
    serializer_class = InitiativeMediaSerializer
    permission_classes = [IsEditorOrAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        """P20: Carga multipart con validación binaria para medios de iniciativas."""
        AuditService.set_db_actor_session(self.request.user)
        uploaded_file = self.request.FILES.get('file') or self.request.FILES.get('archivo')
        if uploaded_file:
            import os
            from django.core.files.storage import default_storage
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ('.jpg', '.jpeg', '.png', '.webp', '.mp4', '.pdf'):
                raise ValidationError({'file': 'Formato no permitido. Use JPG, PNG, WEBP, MP4 o PDF.'})
            if uploaded_file.size > 15 * 1024 * 1024:
                raise ValidationError({'file': 'El archivo excede el tamaño máximo permitido (15MB).'})
            iniciativa_id = self.request.data.get('iniciativa') or getattr(serializer.validated_data.get('iniciativa'), 'id', 'general')
            save_name = f'initiatives/{iniciativa_id}/{uploaded_file.name}'
            saved_path = default_storage.save(save_name, uploaded_file)
            media = serializer.save(ruta_archivo=saved_path)
        else:
            media = serializer.save()

        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='iniciativas',
            target_model='iniciativa_multimedia',
            target_id=media.pk,
            description=f'Carga de multimedia para iniciativa {media.iniciativa_id}',
            request=self.request,
        )

    def perform_destroy(self, instance):
        AuditService.set_db_actor_session(self.request.user)
        media_id = instance.pk
        ini_id = instance.iniciativa_id
        instance.delete()
        AuditService.log(
            actor=self.request.user,
            action='delete',
            module='iniciativas',
            target_model='iniciativa_multimedia',
            target_id=media_id,
            description=f'Eliminación de multimedia {media_id} de iniciativa {ini_id}',
            request=self.request,
        )


class AdminInitiativeMetricViewSet(viewsets.ModelViewSet):
    queryset = InitiativeMetric.objects.select_related('edicion').all()
    serializer_class = InitiativeMetricSerializer
    permission_classes = [IsEditorOrAdmin]

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        metric = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='iniciativas',
            target_model='iniciativa_indicadores',
            target_id=metric.pk,
            description=f'Creación de indicador "{metric.nombre}" en edición {metric.edicion_id}',
            request=self.request,
        )

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        metric = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='update',
            module='iniciativas',
            target_model='iniciativa_indicadores',
            target_id=metric.pk,
            description=f'Actualización de indicador "{metric.nombre}"',
            request=self.request,
        )

    def perform_destroy(self, instance):
        AuditService.set_db_actor_session(self.request.user)
        m_id = instance.pk
        ed_id = instance.edicion_id
        instance.delete()
        AuditService.log(
            actor=self.request.user,
            action='delete',
            module='iniciativas',
            target_model='iniciativa_indicadores',
            target_id=m_id,
            description=f'Eliminación de indicador {m_id} en edición {ed_id}',
            request=self.request,
        )


class AdminInitiativeCommunityViewSet(viewsets.ModelViewSet):
    queryset = InitiativeCommunity.objects.select_related('edicion', 'comunidad').all()
    serializer_class = InitiativeCommunitySerializer
    permission_classes = [IsEditorOrAdmin]

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        rel = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='iniciativas',
            target_model='iniciativa_comunidades',
            target_id=rel.pk,
            description=f'Vinculación de comunidad {rel.comunidad_id} a edición {rel.edicion_id}',
            request=self.request,
        )

    def perform_destroy(self, instance):
        AuditService.set_db_actor_session(self.request.user)
        r_id = instance.pk
        instance.delete()
        AuditService.log(
            actor=self.request.user,
            action='delete',
            module='iniciativas',
            target_model='iniciativa_comunidades',
            target_id=r_id,
            description=f'Desvinculación de comunidad en iniciativa',
            request=self.request,
        )


class AdminInitiativeCaseLinkViewSet(viewsets.ModelViewSet):
    queryset = InitiativeCaseLink.objects.select_related('edicion', 'caso').all()
    serializer_class = InitiativeCaseLinkSerializer
    permission_classes = [IsEditorOrAdmin]

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        link = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='iniciativas',
            target_model='iniciativa_casos',
            target_id=link.pk,
            description=f'Vinculación de caso {link.caso_id} a edición {link.edicion_id}',
            request=self.request,
        )

    def perform_destroy(self, instance):
        AuditService.set_db_actor_session(self.request.user)
        l_id = instance.pk
        instance.delete()
        AuditService.log(
            actor=self.request.user,
            action='delete',
            module='iniciativas',
            target_model='iniciativa_casos',
            target_id=l_id,
            description=f'Desvinculación de caso en iniciativa',
            request=self.request,
        )
