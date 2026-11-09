from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import (
    AdminRoleViewSet,
    AdminUserViewSet,
    ChangePasswordView,
    CitizenRegisterView,
    LoginView,
    LogoutView,
    MePhotoView,
    MePreferencesView,
    MeProfileView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    PasswordResetValidateView,
    ResponsibleScopeAssignmentViewSet,
)
from apps.audit.views import (
    AdminAuditEventDetailView,
    AdminAuditEventListView,
    AdminAuditLogViewSet,
)
from apps.cases.views import (
    AdminCaseCategoryViewSet,
    AdminCaseEvidenceViewSet,
    AdminCaseReportExportCSVView,
    AdminCaseReportView,
    AdminCaseViewSet,
    CitizenCaseViewSet,
    CitizenDashboardView,
    FollowedCaseView,
    PublicCaseCategoryListView,
    PublicCaseCategoryNamesView,
    PublicCaseDetailView,
    PublicCaseEvidenceView,
    PublicCaseHistoryView,
    PublicCaseListView,
    PublicCaseMapGeoJSONView,
    PublicCaseOptionsView,
    PublicCaseStatusListView,
)
from apps.communications.views import (
    AdminCaseCommentModerationViewSet,
    AdminEventProposalViewSet,
    AdminSiteSettingViewSet,
    CasePrivateMessageListCreateView,
    CasePrivateMessageMarkReadView,
    CitizenCaseCommentCreateView,
    MeConversationListView,
    NewsletterConfirmView,
    NewsletterSubscribeView,
    NewsletterUnsubscribeView,
    PublicCaseCommentListView,
    PublicEventProposalCreateView,
    PublicSiteInfoView,
    PublicSiteSettingListView,
)
from apps.initiatives.views import (
    AdminInitiativeActivityViewSet,
    AdminInitiativeCaseLinkViewSet,
    AdminInitiativeCommunityViewSet,
    AdminInitiativeEditionViewSet,
    AdminInitiativeMediaViewSet,
    AdminInitiativeMetricViewSet,
    AdminInitiativeViewSet,
    PublicInitiativeCategoryListView,
    PublicInitiativeDetailView,
    PublicInitiativeEditionActivityListView,
    PublicInitiativeEditionDetailView,
    PublicInitiativeEditionListView,
    PublicInitiativeGalleryView,
    PublicInitiativeListView,
)
from apps.news.views import (
    AdminMetricsDashboardView,
    AdminNewsArticleViewSet,
    AdminNewsCategoryViewSet,
    AdminNewsMediaViewSet,
    PublicHomeSummaryView,
    PublicNewsCategoryListView,
    PublicNewsDetailView,
    PublicNewsListView,
)
from apps.notifications.views import UserNotificationViewSet
from apps.territories.views import (
    AdminBasinViewSet,
    AdminCommunityViewSet,
    AdminDepartmentViewSet,
    AdminMunicipalityViewSet,
    PublicBasinListView,
    PublicCommunityListView,
    PublicDepartmentListView,
    PublicMunicipalityListView,
)

# Citizen Portal Router (/api/v1/citizen/ and /api/v1/me/)
citizen_router = DefaultRouter()
citizen_router.register('cases', CitizenCaseViewSet, basename='citizen-cases')
citizen_router.register('notifications', UserNotificationViewSet, basename='citizen-notifications')

me_router = DefaultRouter()
me_router.register('cases', CitizenCaseViewSet, basename='me-cases')
me_router.register('notifications', UserNotificationViewSet, basename='me-notifications')

# Administrative Panel Router (/api/v1/admin/)
admin_router = DefaultRouter()
admin_router.register('users', AdminUserViewSet, basename='admin-users')
admin_router.register('roles', AdminRoleViewSet, basename='admin-roles')
admin_router.register('scope-assignments', ResponsibleScopeAssignmentViewSet, basename='admin-scope-assignments')
admin_router.register('departments', AdminDepartmentViewSet, basename='admin-departments')
admin_router.register('municipalities', AdminMunicipalityViewSet, basename='admin-municipalities')
admin_router.register('communities', AdminCommunityViewSet, basename='admin-communities')
admin_router.register('basins', AdminBasinViewSet, basename='admin-basins')
admin_router.register('case-categories', AdminCaseCategoryViewSet, basename='admin-case-categories')
admin_router.register('cases', AdminCaseViewSet, basename='admin-cases')
admin_router.register('evidence', AdminCaseEvidenceViewSet, basename='admin-evidence')
admin_router.register('comments', AdminCaseCommentModerationViewSet, basename='admin-comments')
admin_router.register('event-proposals', AdminEventProposalViewSet, basename='admin-event-proposals')
admin_router.register('proposals', AdminEventProposalViewSet, basename='admin-proposals')
admin_router.register('initiatives', AdminInitiativeViewSet, basename='admin-initiatives')
admin_router.register('initiative-editions', AdminInitiativeEditionViewSet, basename='admin-initiative-editions')
admin_router.register('initiative-activities', AdminInitiativeActivityViewSet, basename='admin-initiative-activities')
admin_router.register('initiative-communities', AdminInitiativeCommunityViewSet, basename='admin-initiative-communities')
admin_router.register('initiative-case-links', AdminInitiativeCaseLinkViewSet, basename='admin-initiative-case-links')
admin_router.register('initiative-media', AdminInitiativeMediaViewSet, basename='admin-initiative-media')
admin_router.register('initiative-metrics', AdminInitiativeMetricViewSet, basename='admin-initiative-metrics')
admin_router.register('news-categories', AdminNewsCategoryViewSet, basename='admin-news-categories')
admin_router.register('news', AdminNewsArticleViewSet, basename='admin-news')
admin_router.register('news-media', AdminNewsMediaViewSet, basename='admin-news-media')
admin_router.register('settings', AdminSiteSettingViewSet, basename='admin-settings')
admin_router.register('audit-logs', AdminAuditLogViewSet, basename='admin-audit-logs')

urlpatterns = [
    # OpenAPI 3 Schema and Swagger UI for Angular integration
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),

    # =========================================================================
    # 4. Autenticación y Recuperación (/api/v1/auth/) — AUTH-01..07
    # =========================================================================
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/register/', CitizenRegisterView.as_view(), name='auth-register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/password-reset/request/', PasswordResetRequestView.as_view(), name='auth-password-reset-request'),
    path('auth/password-reset/validate/', PasswordResetValidateView.as_view(), name='auth-password-reset-validate'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
    # Aliases compatibles previos
    path('auth/me/', MeProfileView.as_view(), name='auth-me'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='auth-change-password'),

    # =========================================================================
    # 5. Perfil y Cuenta Propia (/api/v1/me/) — ME-01..05, CIT-01..08, NOT-01..03, MSG-01, MAP-08..10
    # =========================================================================
    path('me/', MeProfileView.as_view(), name='me-profile'),
    path('me/photo/', MePhotoView.as_view(), name='me-photo'),
    path('me/change-password/', ChangePasswordView.as_view(), name='me-change-password'),
    path('me/preferences/', MePreferencesView.as_view(), name='me-preferences'),
    path('me/conversations/', MeConversationListView.as_view(), name='me-conversations'),
    path('me/followed-cases/', FollowedCaseView.as_view(), name='me-followed-cases-list'),
    path('me/followed-cases/<uuid:case_id>/', FollowedCaseView.as_view(), name='me-followed-cases-detail'),
    path('me/', include(me_router.urls)),

    # =========================================================================
    # 6. Catálogos Territoriales y Maestros (/api/v1/catalogs/) — CAT-01..08
    # =========================================================================
    path('catalogs/departments/', PublicDepartmentListView.as_view(), name='catalogs-departments'),
    path('catalogs/municipalities/', PublicMunicipalityListView.as_view(), name='catalogs-municipalities'),
    path('catalogs/communities/', PublicCommunityListView.as_view(), name='catalogs-communities'),
    path('catalogs/basins/', PublicBasinListView.as_view(), name='catalogs-basins'),
    path('catalogs/case-types/', PublicCaseCategoryListView.as_view(), name='catalogs-case-types'),
    path('catalogs/case-categories/', PublicCaseCategoryNamesView.as_view(), name='catalogs-case-categories'),
    path('catalogs/case-statuses/', PublicCaseStatusListView.as_view(), name='catalogs-case-statuses'),
    path('catalogs/case-options/', PublicCaseOptionsView.as_view(), name='catalogs-case-options'),

    # =========================================================================
    # 7 & 8. Portal Público, Noticias, Iniciativas y Mapa (/api/v1/public/) — PUB-01..11, INI-01..03, MAP-01..06
    # =========================================================================
    path('public/home/', PublicHomeSummaryView.as_view(), name='public-home'),
    path('public/site-info/', PublicSiteInfoView.as_view(), name='public-site-info'),
    path('public/territories/departments/', PublicDepartmentListView.as_view(), name='public-departments'),
    path('public/territories/municipalities/', PublicMunicipalityListView.as_view(), name='public-municipalities'),
    path(
        'public/territories/municipalities/<uuid:municipality_id>/communities/',
        PublicCommunityListView.as_view(),
        name='public-municipality-communities',
    ),
    path('public/territories/communities/', PublicCommunityListView.as_view(), name='public-communities'),
    path('public/case-categories/', PublicCaseCategoryListView.as_view(), name='public-case-categories'),
    path('public/case-statuses/', PublicCaseStatusListView.as_view(), name='public-case-statuses'),

    # Mapa y Casos Públicos (MAP-01..06)
    path('public/cases/map/', PublicCaseMapGeoJSONView.as_view(), name='public-cases-map'),
    path('public/cases/geojson/', PublicCaseMapGeoJSONView.as_view(), name='public-cases-geojson'),
    path('public/cases/', PublicCaseListView.as_view(), name='public-cases-list'),
    path('public/cases/<uuid:case_id>/history/', PublicCaseHistoryView.as_view(), name='public-cases-history'),
    path('public/cases/<uuid:case_id>/evidences/', PublicCaseEvidenceView.as_view(), name='public-cases-evidences'),
    path('public/cases/<uuid:case_id>/comments/', PublicCaseCommentListView.as_view(), name='public-cases-comments'),
    path('public/cases/<str:lookup>/', PublicCaseDetailView.as_view(), name='public-cases-detail'),

    # Iniciativas Públicas (PUB-06..10, INI-01..03)
    path('public/initiatives/', PublicInitiativeListView.as_view(), name='public-initiatives-list'),
    path('public/initiatives/categories/', PublicInitiativeCategoryListView.as_view(), name='public-initiatives-categories'),
    path('public/initiatives/proposals/', PublicEventProposalCreateView.as_view(), name='public-initiatives-proposals'),
    path('public/initiatives/gallery/', PublicInitiativeGalleryView.as_view(), name='public-initiatives-gallery'),
    path(
        'public/initiatives/<str:lookup>/editions/',
        PublicInitiativeEditionListView.as_view(),
        name='public-initiatives-editions',
    ),
    path(
        'public/initiatives/<str:lookup>/editions/<uuid:edition_id>/',
        PublicInitiativeEditionDetailView.as_view(),
        name='public-initiatives-edition-detail',
    ),
    path(
        'public/initiatives/<str:lookup>/editions/<uuid:edition_id>/activities/',
        PublicInitiativeEditionActivityListView.as_view(),
        name='public-initiatives-edition-activities',
    ),
    path('public/initiatives/<str:lookup>/', PublicInitiativeDetailView.as_view(), name='public-initiatives-detail'),

    # Noticias Públicas y Boletín (PUB-03..05, PUB-11)
    path('public/news/categories/', PublicNewsCategoryListView.as_view(), name='public-news-categories-v12'),
    path('public/news-categories/', PublicNewsCategoryListView.as_view(), name='public-news-categories'),
    path('public/news/', PublicNewsListView.as_view(), name='public-news-list'),
    path('public/news/<str:lookup>/', PublicNewsDetailView.as_view(), name='public-news-detail'),
    path('public/newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='public-newsletter-subscribe'),
    path('public/newsletter/confirm/', NewsletterConfirmView.as_view(), name='public-newsletter-confirm'),
    path('public/newsletter/unsubscribe/', NewsletterUnsubscribeView.as_view(), name='public-newsletter-unsubscribe'),

    path('public/event-proposals/', PublicEventProposalCreateView.as_view(), name='public-event-proposals'),
    path('public/settings/', PublicSiteSettingListView.as_view(), name='public-settings'),

    # =========================================================================
    # 10. Mensajería Privada y Comentarios de Caso (/api/v1/cases/) — MAP-07, MSG-02..04
    # =========================================================================
    path('cases/<uuid:case_id>/comments/', CitizenCaseCommentCreateView.as_view(), name='case-comments-create'),
    path('cases/<uuid:case_id>/messages/', CasePrivateMessageListCreateView.as_view(), name='case-messages'),
    path('cases/<uuid:case_id>/messages/mark-read/', CasePrivateMessageMarkReadView.as_view(), name='case-messages-mark-read'),

    # =========================================================================
    # Portal Ciudadano Compatible (/api/v1/citizen/)
    # =========================================================================
    path('citizen/dashboard/', CitizenDashboardView.as_view(), name='citizen-dashboard'),
    path(
        'citizen/cases/<uuid:case_id>/messages/',
        CasePrivateMessageListCreateView.as_view(),
        name='citizen-case-messages',
    ),
    path(
        'citizen/cases/<uuid:case_id>/comments/',
        CitizenCaseCommentCreateView.as_view(),
        name='citizen-case-comments',
    ),
    path('citizen/', include(citizen_router.urls)),

    # =========================================================================
    # 11-14. Panel Administrativo, Reportes y Auditoría (/api/v1/admin/) — ADM-01..11, REP-01..02, AUD-01..02, USR-01..07
    # =========================================================================
    path('admin/metrics/dashboard/', AdminMetricsDashboardView.as_view(), name='admin-metrics-dashboard'),
    path('admin/reports/cases/', AdminCaseReportView.as_view(), name='admin-reports-cases'),
    path('admin/reports/cases/export/', AdminCaseReportExportCSVView.as_view(), name='admin-reports-cases-export'),
    path('admin/audit/events/', AdminAuditEventListView.as_view(), name='admin-audit-events'),
    path('admin/audit/events/<str:event_ref>/', AdminAuditEventDetailView.as_view(), name='admin-audit-event-detail'),
    path(
        'admin/cases/<uuid:case_id>/messages/',
        CasePrivateMessageListCreateView.as_view(),
        name='admin-case-messages',
    ),
    path('admin/', include(admin_router.urls)),
]
