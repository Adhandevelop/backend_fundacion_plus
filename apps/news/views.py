from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, permissions, serializers as drf_serializers, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsEditorOrAdmin, IsResponsibleOrAdmin
from apps.audit.services import AuditService
from apps.cases.models import Case, CaseCorrectionRequest, CaseStatus
from apps.communications.models import CaseComment, EventProposal, SiteSetting
from apps.initiatives.models import Initiative, InitiativeActivity
from apps.initiatives.serializers import InitiativeListSerializer
from apps.news.models import NewsArticle, NewsCategory, NewsMedia
from apps.news.serializers import (
    NewsArticleDetailSerializer,
    NewsArticleListSerializer,
    NewsCategorySerializer,
    NewsMediaSerializer,
)
from apps.territories.models import Community, Municipality


class PublicNewsCategoryListView(generics.ListAPIView):
    """CAT-07 (AMP-01): GET /api/v1/catalogs/news-categories/ (y /api/v1/public/news/categories/)"""
    queryset = NewsCategory.objects.filter(activa=True)
    serializer_class = NewsCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class PublicNewsListView(generics.ListAPIView):
    """PUB-03 (AMP-01): GET /api/v1/public/news/"""
    serializer_class = NewsArticleListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = (
            NewsArticle.objects.filter(estado_publicacion=NewsArticle.EstadoPublicacion.PUBLICADA)
            .select_related('categoria', 'autor', 'iniciativa_relacionada')
            .prefetch_related('multimedia')
        )
        params = self.request.query_params
        if cat := (params.get('id_categoria') or params.get('categoria') or params.get('category')):
            qs = qs.filter(categoria_id=cat)
        if cat_slug := params.get('categoria_slug'):
            qs = qs.filter(categoria__slug=cat_slug)
        if destacada := (params.get('destacada') or params.get('is_featured')):
            qs = qs.filter(destacada=destacada.lower() == 'true')
        if search := params.get('search'):
            qs = qs.filter(Q(titulo__icontains=search) | Q(extracto__icontains=search))
        return qs


class PublicNewsDetailView(generics.RetrieveAPIView):
    """PUB-04 (AMP-01): GET /api/v1/public/news/{slug}/"""
    serializer_class = NewsArticleDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        lookup = self.kwargs['lookup']
        qs = (
            NewsArticle.objects.filter(estado_publicacion=NewsArticle.EstadoPublicacion.PUBLICADA)
            .select_related('categoria', 'autor', 'iniciativa_relacionada')
            .prefetch_related('multimedia')
        )
        article = qs.filter(slug=lookup).first()
        if not article:
            article = get_object_or_404(qs, pk=lookup)
        return article


class AdminNewsCategoryViewSet(viewsets.ModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    permission_classes = [IsEditorOrAdmin]


class AdminNewsArticleViewSet(viewsets.ModelViewSet):
    serializer_class = NewsArticleDetailSerializer
    permission_classes = [IsEditorOrAdmin]

    def get_queryset(self):
        qs = (
            NewsArticle.objects.select_related('categoria', 'autor', 'iniciativa_relacionada')
            .prefetch_related('multimedia')
            .all()
        )
        params = self.request.query_params
        if pub_status := (params.get('estado_publicacion') or params.get('publication_status')):
            status_map = {
                'draft': NewsArticle.EstadoPublicacion.BORRADOR,
                'published': NewsArticle.EstadoPublicacion.PUBLICADA,
                'archived': NewsArticle.EstadoPublicacion.ARCHIVADA,
            }
            resolved = status_map.get(pub_status.lower(), pub_status.lower())
            qs = qs.filter(estado_publicacion=resolved)
        return qs

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        article = serializer.save(autor=self.request.user)
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='noticias',
            target_model='noticias',
            target_id=article.pk,
            description=f'Creación de noticia: {article.titulo}',
            request=self.request,
        )

    def perform_update(self, serializer):
        """P18: Auditoría de transiciones y cambios en noticias."""
        AuditService.set_db_actor_session(self.request.user)
        prev_status = serializer.instance.estado_publicacion
        article = serializer.save()
        new_status = article.estado_publicacion
        AuditService.log(
            actor=self.request.user,
            action='update',
            module='noticias',
            target_model='noticias',
            target_id=article.pk,
            description=f'Actualización de noticia "{article.titulo}" (estado: {prev_status} -> {new_status})',
            previous_data={'estado_publicacion': prev_status},
            new_data={'estado_publicacion': new_status},
            request=self.request,
        )

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        """P18: Publicar noticia con registro en auditoría."""
        article = self.get_object()
        AuditService.set_db_actor_session(request.user)
        prev_status = article.estado_publicacion
        article.estado_publicacion = NewsArticle.EstadoPublicacion.PUBLICADA
        if not article.fecha_publicacion:
            article.fecha_publicacion = timezone.now()
        article.save(update_fields=['estado_publicacion', 'fecha_publicacion', 'fecha_actualizacion'])
        AuditService.log(
            actor=request.user,
            action='publish',
            module='noticias',
            target_model='noticias',
            target_id=article.pk,
            description=f'Publicación de noticia: {article.titulo}',
            previous_data={'estado_publicacion': prev_status},
            new_data={'estado_publicacion': article.estado_publicacion},
            request=request,
        )
        return Response(NewsArticleDetailSerializer(article).data)

    @action(detail=True, methods=['post'], url_path='archive')
    def archive(self, request, pk=None):
        """P18: Archivar noticia con registro en auditoría."""
        article = self.get_object()
        AuditService.set_db_actor_session(request.user)
        prev_status = article.estado_publicacion
        article.estado_publicacion = NewsArticle.EstadoPublicacion.ARCHIVADA
        article.save(update_fields=['estado_publicacion', 'fecha_actualizacion'])
        AuditService.log(
            actor=request.user,
            action='archive',
            module='noticias',
            target_model='noticias',
            target_id=article.pk,
            description=f'Archivado de noticia: {article.titulo}',
            previous_data={'estado_publicacion': prev_status},
            new_data={'estado_publicacion': article.estado_publicacion},
            request=request,
        )
        return Response(NewsArticleDetailSerializer(article).data)


class AdminNewsMediaViewSet(viewsets.ModelViewSet):
    queryset = NewsMedia.objects.select_related('noticia').all()
    serializer_class = NewsMediaSerializer
    permission_classes = [IsEditorOrAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        """P18 y P21: Carga multipart/form-data con validación binaria y sanitización en serializer."""
        AuditService.set_db_actor_session(self.request.user)
        media = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='noticias',
            target_model='noticia_multimedia',
            target_id=media.pk,
            description=f'Carga de multimedia para noticia {media.noticia_id}',
            request=self.request,
        )

    def perform_destroy(self, instance):
        AuditService.set_db_actor_session(self.request.user)
        m_id = instance.pk
        n_id = instance.noticia_id
        instance.delete()
        AuditService.log(
            actor=self.request.user,
            action='delete',
            module='noticias',
            target_model='noticia_multimedia',
            target_id=m_id,
            description=f'Eliminación de multimedia {m_id} en noticia {n_id}',
            request=self.request,
        )


class PublicHomeSummaryView(APIView):
    """
    PUB-02: GET /api/v1/public/home/
    Agrega datos institucionales desde plus.configuracion_plataforma, indicadores reales validados,
    iniciativas destacadas (plus.iniciativas) y noticias recientes (plus.noticias) para el Home en Angular.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='PublicHomeSummaryResponse',
                fields={
                    'institution': drf_serializers.DictField(),
                    'verified_indicators': drf_serializers.DictField(),
                    'featured_initiatives': InitiativeListSerializer(many=True),
                    'recent_news': NewsArticleListSerializer(many=True),
                    'site_settings': drf_serializers.DictField(),
                },
            )
        },
        summary='Resumen de portada institucional, indicadores verificados, iniciativas y noticias (PUB-02)',
    )
    def get(self, request):
        approved_cases = Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO)
        published_initiatives = Initiative.objects.filter(
            estado_publicacion=Initiative.EstadoPublicacion.PUBLICADA
        ).prefetch_related('multimedia', 'ediciones__indicadores')
        featured_initiatives = published_initiatives.filter(destacada=True)[:6]
        recent_news = (
            NewsArticle.objects.filter(estado_publicacion=NewsArticle.EstadoPublicacion.PUBLICADA)
            .select_related('categoria', 'autor', 'iniciativa_relacionada')
            .prefetch_related('multimedia')[:4]
        )
        settings_map = {s.clave: s.valor for s in SiteSetting.objects.all()}

        default_institution = {
            'corporation_name': settings_map.get('institucion.nombre', 'Corporación Pluralismo Social'),
            'acronym': settings_map.get('institucion.sigla', 'PLUS'),
            'representative_name': settings_map.get('institucion.representante_nombre', 'JUAN DAVID MARTINEZ BOLAÑO'),
            'representative_role': settings_map.get('institucion.representante_cargo', 'CEO de la Corporación Pluralismo Social'),
            'mission': settings_map.get(
                'institucion.mision',
                (
                    'Fortalecer la participación ciudadana, la veeduría social y el acompañamiento '
                    'territorial de las comunidades mediante gestión transparente e iniciativas de impacto.'
                ),
            ),
        }

        hero_setting = settings_map.get('INSTITUTION_HERO')
        institution_data = dict(default_institution)
        if isinstance(hero_setting, dict):
            institution_data.update(hero_setting)
        elif isinstance(hero_setting, str):
            institution_data['image_url'] = hero_setting

        return Response({
            'institution': institution_data,
            'verified_indicators': {
                'published_cases_count': approved_cases.count(),
                'resolved_cases_count': approved_cases.filter(
                    estado__nombre__in=[CaseStatus.Nombre.RESUELTO, CaseStatus.Nombre.CERRADO]
                ).count(),
                'active_municipalities_count': Municipality.objects.count(),
                'active_communities_count': Community.objects.filter(activo=True).count(),
                'published_initiatives_count': published_initiatives.count(),
                'completed_activities_count': InitiativeActivity.objects.filter(
                    estado=InitiativeActivity.Estado.REALIZADA
                ).count(),
            },
            'featured_initiatives': InitiativeListSerializer(
                featured_initiatives, many=True, context={'request': request}
            ).data,
            'recent_news': NewsArticleListSerializer(
                recent_news, many=True, context={'request': request}
            ).data,
            'site_settings': settings_map,
        })


class AdminMetricsDashboardView(APIView):
    """
    ADM-01: GET /api/v1/admin/dashboard/ (y /api/v1/admin/metrics/dashboard/)
    Indicadores operativos del Panel Administrativo desde las tablas de `plus`.
    """
    permission_classes = [IsResponsibleOrAdmin]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='AdminMetricsDashboardResponse',
                fields={
                    'cases': drf_serializers.DictField(),
                    'moderation_queues': drf_serializers.DictField(),
                    'territories': drf_serializers.DictField(),
                    'content': drf_serializers.DictField(),
                    'users': drf_serializers.DictField(),
                },
            )
        },
        summary='Indicadores operativos del Dashboard Administrativo (ADM-01)',
    )
    def get(self, request):
        scope_param = request.query_params.get('scope', 'global').lower()
        cases_base = Case.objects.all()
        if scope_param == 'assigned':
            cases_base = cases_base.filter(asignaciones__responsable=request.user, asignaciones__activo=True)

        cases_by_pub = dict(
            cases_base.values_list('estado_publicacion').annotate(total=Count('id'))
        )
        cases_by_estado = dict(
            cases_base.values_list('estado__nombre').annotate(total=Count('id'))
        )
        cases_by_prio = dict(
            cases_base.values_list('prioridad').annotate(total=Count('id'))
        )
        my_assigned_count = Case.objects.filter(asignaciones__responsable=request.user, asignaciones__activo=True).count()

        return Response({
            'scope': scope_param,
            'cases': {
                'total': cases_base.count(),
                'assigned_to_me': my_assigned_count,
                'by_estado_publicacion': cases_by_pub,
                'by_estado_operativo': cases_by_estado,
                'by_prioridad': cases_by_prio,
                'open_correction_requests': CaseCorrectionRequest.objects.filter(
                    estado=CaseCorrectionRequest.Estado.ABIERTA,
                    caso__in=cases_base,
                ).count(),
            },
            'moderation_queues': {
                'pending_cases': Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.PENDIENTE).count(),
                'pending_comments': CaseComment.objects.filter(
                    estado_moderacion=CaseComment.EstadoModeracion.PENDIENTE
                ).count(),
                'pending_proposals': EventProposal.objects.filter(
                    estado=EventProposal.Estado.PENDIENTE
                ).count(),
            },
            'territories': {
                'municipalities': Municipality.objects.count(),
                'communities': Community.objects.filter(activo=True).count(),
            },
            'content': {
                'initiatives_published': Initiative.objects.filter(
                    estado_publicacion=Initiative.EstadoPublicacion.PUBLICADA
                ).count(),
                'initiatives_draft': Initiative.objects.filter(
                    estado_publicacion=Initiative.EstadoPublicacion.BORRADOR
                ).count(),
                'news_published': NewsArticle.objects.filter(
                    estado_publicacion=NewsArticle.EstadoPublicacion.PUBLICADA
                ).count(),
            },
            'users': {
                'total_active': User.objects.filter(estado=User.Estado.ACTIVO).count(),
            },
        })
