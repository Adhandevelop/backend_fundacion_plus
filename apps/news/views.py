from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsAdminOrSuperAdmin, IsEditorOrAdmin
from apps.audit.services import AuditService
from apps.cases.models import Case, CaseStatus
from apps.communications.models import CaseComment, EventProposal, SiteSetting
from apps.initiatives.models import Initiative, InitiativeActivity
from apps.initiatives.serializers import InitiativeListSerializer
from apps.news.models import NewsArticle, NewsCategory
from apps.news.serializers import (
    NewsArticleDetailSerializer,
    NewsArticleListSerializer,
    NewsCategorySerializer,
)
from apps.territories.models import Community, Municipality


class PublicNewsCategoryListView(generics.ListAPIView):
    queryset = NewsCategory.objects.filter(is_active=True)
    serializer_class = NewsCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class PublicNewsListView(generics.ListAPIView):
    serializer_class = NewsArticleListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = NewsArticle.objects.filter(
            publication_status=NewsArticle.PublicationStatus.PUBLISHED
        ).select_related('category', 'author', 'related_initiative')
        params = self.request.query_params
        if category := params.get('category'):
            qs = qs.filter(category_id=category)
        if is_featured := params.get('is_featured'):
            qs = qs.filter(is_featured=is_featured.lower() == 'true')
        if search := params.get('search'):
            qs = qs.filter(title__icontains=search) | qs.filter(summary__icontains=search)
        return qs


class PublicNewsDetailView(generics.RetrieveAPIView):
    serializer_class = NewsArticleDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        lookup = self.kwargs['lookup']
        qs = NewsArticle.objects.filter(
            publication_status=NewsArticle.PublicationStatus.PUBLISHED
        ).select_related('category', 'author', 'related_initiative')
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
        qs = NewsArticle.objects.select_related('category', 'author', 'related_initiative').all()
        if pub_status := self.request.query_params.get('publication_status'):
            qs = qs.filter(publication_status=pub_status.upper())
        return qs

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        article = serializer.save(author=self.request.user)
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='noticias',
            target_model='news_articles',
            target_id=article.pk,
            description=f'Creación de noticia: {article.title}',
            request=self.request,
        )


class PublicHomeSummaryView(APIView):
    """
    GET /api/v1/public/home/
    Agrega datos institucionales desde plus.configuracion_plataforma, indicadores reales validados,
    iniciativas destacadas (plus.iniciativas) y noticias recientes para el Home en Angular.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        approved_cases = Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO)
        published_initiatives = Initiative.objects.filter(
            estado_publicacion=Initiative.EstadoPublicacion.PUBLICADA
        ).prefetch_related('multimedia', 'ediciones__indicadores')
        featured_initiatives = published_initiatives.filter(destacada=True)[:6]
        recent_news = NewsArticle.objects.filter(
            publication_status=NewsArticle.PublicationStatus.PUBLISHED
        ).select_related('category', 'author', 'related_initiative')[:4]
        settings_map = {s.clave: s.valor for s in SiteSetting.objects.all()}

        default_institution = {
            'corporation_name': settings_map.get('institucion.nombre', 'Corporación Pluralismo Social'),
            'acronym': 'PLUS',
            'representative_name': 'Luis Alberto Muñoz Granada',
            'representative_role': 'Representante Legal y Director Institucional',
            'mission': (
                'Fortalecer la participación ciudadana, la veeduría social y el acompañamiento '
                'territorial de las comunidades mediante gestión transparente e iniciativas de impacto.'
            ),
        }

        return Response({
            'institution': settings_map.get('INSTITUTION_HERO', default_institution),
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
    GET /api/v1/admin/metrics/dashboard/
    Indicadores operativos del Panel Administrativo desde las 30 tablas de `plus`.
    """
    permission_classes = [IsAdminOrSuperAdmin]

    def get(self, request):
        cases_by_pub = dict(
            Case.objects.values_list('estado_publicacion').annotate(total=Count('id'))
        )
        cases_by_estado = dict(
            Case.objects.values_list('estado__nombre').annotate(total=Count('id'))
        )
        cases_by_prio = dict(
            Case.objects.values_list('prioridad').annotate(total=Count('id'))
        )
        return Response({
            'cases': {
                'total': Case.objects.count(),
                'by_estado_publicacion': cases_by_pub,
                'by_estado_operativo': cases_by_estado,
                'by_prioridad': cases_by_prio,
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
                    publication_status=NewsArticle.PublicationStatus.PUBLISHED
                ).count(),
            },
            'users': {
                'total_active': User.objects.filter(estado=User.Estado.ACTIVO).count(),
            },
        })
