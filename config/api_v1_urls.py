from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.accounts.views import (
    AdminRoleViewSet,
    AdminUserViewSet,
    ChangePasswordView,
    CitizenRegisterView,
    LoginView,
    MeProfileView,
)
from apps.audit.views import AdminAuditLogViewSet
from apps.cases.views import (
    AdminCaseCategoryViewSet,
    AdminCaseEvidenceViewSet,
    AdminCaseViewSet,
    CitizenCaseViewSet,
    CitizenDashboardView,
    PublicCaseCategoryListView,
    PublicCaseDetailView,
    PublicCaseListView,
    PublicCaseMapGeoJSONView,
    PublicCaseStatusListView,
)
from apps.communications.views import (
    AdminCaseCommentModerationViewSet,
    AdminEventProposalViewSet,
    AdminSiteSettingViewSet,
    CasePrivateMessageListCreateView,
    CitizenCaseCommentCreateView,
    PublicEventProposalCreateView,
    PublicSiteSettingListView,
)
from apps.initiatives.views import (
    AdminInitiativeActivityViewSet,
    AdminInitiativeEditionViewSet,
    AdminInitiativeMediaViewSet,
    AdminInitiativeMetricViewSet,
    AdminInitiativeViewSet,
    PublicInitiativeDetailView,
    PublicInitiativeListView,
)
from apps.news.views import (
    AdminMetricsDashboardView,
    AdminNewsArticleViewSet,
    AdminNewsCategoryViewSet,
    PublicHomeSummaryView,
    PublicNewsCategoryListView,
    PublicNewsDetailView,
    PublicNewsListView,
)
from apps.notifications.views import UserNotificationViewSet
from apps.territories.views import (
    AdminCommunityViewSet,
    AdminDepartmentViewSet,
    AdminMunicipalityViewSet,
    PublicCommunityListView,
    PublicDepartmentListView,
    PublicMunicipalityListView,
)

# Citizen Portal Router (/api/v1/citizen/)
citizen_router = DefaultRouter()
citizen_router.register('cases', CitizenCaseViewSet, basename='citizen-cases')
citizen_router.register('notifications', UserNotificationViewSet, basename='citizen-notifications')

# Administrative Panel Router (/api/v1/admin/)
admin_router = DefaultRouter()
admin_router.register('users', AdminUserViewSet, basename='admin-users')
admin_router.register('roles', AdminRoleViewSet, basename='admin-roles')
admin_router.register('departments', AdminDepartmentViewSet, basename='admin-departments')
admin_router.register('municipalities', AdminMunicipalityViewSet, basename='admin-municipalities')
admin_router.register('communities', AdminCommunityViewSet, basename='admin-communities')
admin_router.register('case-categories', AdminCaseCategoryViewSet, basename='admin-case-categories')
admin_router.register('cases', AdminCaseViewSet, basename='admin-cases')
admin_router.register('evidence', AdminCaseEvidenceViewSet, basename='admin-evidence')
admin_router.register('comments', AdminCaseCommentModerationViewSet, basename='admin-comments')
admin_router.register('event-proposals', AdminEventProposalViewSet, basename='admin-event-proposals')
admin_router.register('initiatives', AdminInitiativeViewSet, basename='admin-initiatives')
admin_router.register('initiative-editions', AdminInitiativeEditionViewSet, basename='admin-initiative-editions')
admin_router.register('initiative-activities', AdminInitiativeActivityViewSet, basename='admin-initiative-activities')
admin_router.register('initiative-media', AdminInitiativeMediaViewSet, basename='admin-initiative-media')
admin_router.register('initiative-metrics', AdminInitiativeMetricViewSet, basename='admin-initiative-metrics')
admin_router.register('news-categories', AdminNewsCategoryViewSet, basename='admin-news-categories')
admin_router.register('news', AdminNewsArticleViewSet, basename='admin-news')
admin_router.register('settings', AdminSiteSettingViewSet, basename='admin-settings')
admin_router.register('audit-logs', AdminAuditLogViewSet, basename='admin-audit-logs')

urlpatterns = [
    # OpenAPI 3 Schema and Swagger UI for Angular integration
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),

    # 1. Authentication & Identity (/api/v1/auth/)
    path('auth/register/', CitizenRegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/me/', MeProfileView.as_view(), name='auth-me'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='auth-change-password'),

    # 2. Public Portal (/api/v1/public/)
    path('public/home/', PublicHomeSummaryView.as_view(), name='public-home'),
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
    path('public/cases/map/', PublicCaseMapGeoJSONView.as_view(), name='public-cases-map'),
    path('public/cases/', PublicCaseListView.as_view(), name='public-cases-list'),
    path('public/cases/<str:lookup>/', PublicCaseDetailView.as_view(), name='public-cases-detail'),
    path('public/initiatives/', PublicInitiativeListView.as_view(), name='public-initiatives-list'),
    path('public/initiatives/<str:lookup>/', PublicInitiativeDetailView.as_view(), name='public-initiatives-detail'),
    path('public/news-categories/', PublicNewsCategoryListView.as_view(), name='public-news-categories'),
    path('public/news/', PublicNewsListView.as_view(), name='public-news-list'),
    path('public/news/<str:lookup>/', PublicNewsDetailView.as_view(), name='public-news-detail'),
    path('public/event-proposals/', PublicEventProposalCreateView.as_view(), name='public-event-proposals'),
    path('public/settings/', PublicSiteSettingListView.as_view(), name='public-settings'),

    # 3. Citizen Portal (/api/v1/citizen/)
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

    # 4. Administrative Panel (/api/v1/admin/)
    path('admin/metrics/dashboard/', AdminMetricsDashboardView.as_view(), name='admin-metrics-dashboard'),
    path(
        'admin/cases/<uuid:case_id>/messages/',
        CasePrivateMessageListCreateView.as_view(),
        name='admin-case-messages',
    ),
    path('admin/', include(admin_router.urls)),
]
