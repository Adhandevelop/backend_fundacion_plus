from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.accounts.views import AdministrativoProfileView, ClienteProfileView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Versioned REST API for Angular (/api/v1/)
    path('api/v1/', include('config.api_v1_urls')),
    # Legacy-compatible endpoints
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/clientes/me/', ClienteProfileView.as_view(), name='cliente-profile'),
    path('api/administrativos/me/', AdministrativoProfileView.as_view(), name='administrativo-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
