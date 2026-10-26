from django.urls import path

from users_api.views import AdministrativoProfileView, ClienteProfileView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('clientes/me/', ClienteProfileView.as_view(), name='cliente-profile'),
    path('administrativos/me/', AdministrativoProfileView.as_view(), name='administrativo-profile'),
]
