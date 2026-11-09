from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class RevocableJWTAuthentication(JWTAuthentication):
    """
    Autenticación JWT que verifica:
    1. Que el usuario exista y su cuenta esté en estado 'activo' (is_active=True).
    2. Si el token incluye la marca de sesión ('sid'), que coincida con el Token activo
       en servidor (`authtoken_token`). Al cerrar sesión (`POST /api/v1/auth/logout/`),
       cambiar/restablecer contraseña o suspender la cuenta (`PATCH /admin/users/{id}/status/`),
       se elimina el registro en `authtoken_token`, invalidando de inmediato tanto el
       `access` como el `refresh` token.
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        sid = validated_token.get('sid')
        if sid:
            active_key = Token.objects.filter(user=user).values_list('key', flat=True).first()
            if not active_key or active_key[:16] != sid:
                raise InvalidToken('La sesión fue cerrada o revocada en el servidor.')

        return self.enforce_active_user(user), validated_token

    def enforce_active_user(self, user):
        if not user or not user.is_active or getattr(user, 'estado', 'activo') != 'activo':
            raise AuthenticationFailed('La cuenta de usuario se encuentra suspendida o inactiva.', code='user_inactive')
        return user


class RevocableJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'core.authentication.RevocableJWTAuthentication'
    name = 'jwtAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
