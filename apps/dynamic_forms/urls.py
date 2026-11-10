from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.dynamic_forms.views import (
    AdminFormularioViewSet,
    CitizenSubmissionDetailView,
    CitizenSubmissionListView,
    PublicActivationResendView,
    PublicActivationVerifyView,
    PublicFormularioDetailView,
    PublicFormularioSubmitView,
)

admin_router = DefaultRouter()
admin_router.register('forms', AdminFormularioViewSet, basename='admin-forms')

urlpatterns = [
    # Administración (/api/v1/admin/forms/...)
    path('admin/', include(admin_router.urls)),

    # Público (/api/v1/public/forms/...)
    path('public/forms/<slug:slug>/', PublicFormularioDetailView.as_view(), name='public-form-detail'),
    path('public/forms/<slug:slug>/submit/', PublicFormularioSubmitView.as_view(), name='public-form-submit'),
    path('public/forms/activation/verify/', PublicActivationVerifyView.as_view(), name='public-form-activation-verify'),
    path('public/forms/activation/resend/', PublicActivationResendView.as_view(), name='public-form-activation-resend'),

    # Ciudadano (/api/v1/me/forms/...)
    path('me/forms/submissions/', CitizenSubmissionListView.as_view(), name='me-forms-submissions-list'),
    path('me/forms/submissions/<uuid:submission_id>/', CitizenSubmissionDetailView.as_view(), name='me-forms-submissions-detail'),
]
