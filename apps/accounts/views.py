import logging
import os
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models import Q
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, inline_serializer
from rest_framework import generics, permissions, serializers as drf_serializers, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.emails import send_password_reset_email

from apps.accounts.models import (
    ResponsibleScopeAssignment,
    Role,
    User,
    UserPreference,
    UserProfile,
    normalize_role_name,
)
from apps.accounts.permissions import (
    IsAdminOrSuperAdmin,
    IsClientOnly,
    IsModeratorOrAdmin,
    IsResponsibleOrAdmin,
    IsSuperAdmin,
)
from apps.accounts.serializers import (
    AdminUserCreateUpdateSerializer,
    AdminUserStatusSerializer,
    AssignUserRoleSerializer,
    ChangePasswordSerializer,
    CitizenRegistrationSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PasswordResetValidateSerializer,
    ResponsibleScopeAssignmentSerializer,
    RoleSerializer,
    UserMeSerializer,
    UserPreferenceSerializer,
    UserProfileSerializer,
)
from apps.audit.services import AuditService
from core.validators import validate_file_safety


def get_tokens_for_user(user: User) -> dict:
    token_obj, _ = Token.objects.get_or_create(user=user)
    refresh = RefreshToken.for_user(user)
    refresh['correo'] = user.correo
    refresh['roles'] = user.get_role_codes()
    refresh['primary_role'] = user.get_primary_role()
    refresh['sid'] = token_obj.key[:16]
    jwt_cfg = getattr(settings, 'SIMPLE_JWT', {})
    access_lifetime = jwt_cfg.get('ACCESS_TOKEN_LIFETIME')
    refresh_lifetime = jwt_cfg.get('REFRESH_TOKEN_LIFETIME')
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'token': token_obj.key,
        'token_type': 'Bearer',
        'expires_in': int(access_lifetime.total_seconds()) if access_lifetime else 3600,
        'refresh_expires_in': int(refresh_lifetime.total_seconds()) if refresh_lifetime else 604800,
    }


TokenBundleSerializer = inline_serializer(
    name='TokenBundle',
    fields={
        'access': drf_serializers.CharField(),
        'refresh': drf_serializers.CharField(),
        'token': drf_serializers.CharField(),
        'token_type': drf_serializers.CharField(default='Bearer'),
        'expires_in': drf_serializers.IntegerField(),
        'refresh_expires_in': drf_serializers.IntegerField(),
    },
)

AuthSessionResponseSerializer = inline_serializer(
    name='AuthSessionResponse',
    fields={
        'access': drf_serializers.CharField(help_text='Token JWT de acceso (Bearer).'),
        'refresh': drf_serializers.CharField(help_text='Token JWT de renovación.'),
        'token': drf_serializers.CharField(help_text='Token de sesión revocable en servidor.'),
        'token_type': drf_serializers.CharField(default='Bearer'),
        'expires_in': drf_serializers.IntegerField(help_text='Segundos de vigencia del access token.'),
        'refresh_expires_in': drf_serializers.IntegerField(help_text='Segundos de vigencia del refresh token.'),
        'tokens': TokenBundleSerializer,
        'primary_role': drf_serializers.CharField(required=False),
        'roles': drf_serializers.ListField(child=drf_serializers.CharField(), required=False),
        'user': UserMeSerializer(),
    },
)


class RevocableTokenRefreshView(APIView):
    """
    AUTH-03: POST /api/v1/auth/refresh/
    Renueva el JWT validando que la cuenta siga en estado 'activo' y que la sesión ('sid')
    no haya sido cerrada mediante `/auth/logout/` ni revocada por cambio de contraseña/suspensión.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=inline_serializer(
            name='TokenRefreshRequest',
            fields={'refresh': drf_serializers.CharField(help_text='Token JWT refresh vigente.')},
        ),
        responses={
            200: inline_serializer(
                name='TokenRefreshResponse',
                fields={
                    'access': drf_serializers.CharField(),
                    'refresh': drf_serializers.CharField(),
                    'token_type': drf_serializers.CharField(default='Bearer'),
                    'expires_in': drf_serializers.IntegerField(),
                },
            )
        },
        summary='Renovar token JWT verificando estado de cuenta y sesión activa (AUTH-03)',
    )
    def post(self, request):
        raw_refresh = request.data.get('refresh')
        if not raw_refresh:
            return Response(
                {'code': 'validation_error', 'message': 'El campo refresh es obligatorio.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(raw_refresh)
            user_id = refresh.get('user_id')
            user = User.objects.filter(pk=user_id, estado=User.Estado.ACTIVO).first()
            if not user or not user.is_active:
                return Response(
                    {'code': 'user_inactive', 'message': 'La cuenta se encuentra suspendida o inactiva.'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            sid = refresh.get('sid')
            active_key = Token.objects.filter(user=user).values_list('key', flat=True).first()
            if sid and (not active_key or active_key[:16] != sid):
                return Response(
                    {'code': 'token_revoked', 'message': 'La sesión fue cerrada o revocada en el servidor.'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    'access': tokens['access'],
                    'refresh': tokens['refresh'],
                    'token_type': 'Bearer',
                    'expires_in': tokens['expires_in'],
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {'code': 'token_not_valid', 'message': 'El token refresh es inválido o ha expirado.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class CitizenRegisterView(APIView):
    """AUTH-01: POST /api/v1/auth/register/ — Registro ciudadano en plus.usuarios."""
    permission_classes = [permissions.AllowAny]
    serializer_class = CitizenRegistrationSerializer

    @extend_schema(
        request=CitizenRegistrationSerializer,
        responses={201: AuthSessionResponseSerializer},
        summary='Registro de cuenta ciudadana (AUTH-01)',
    )
    def post(self, request):
        serializer = CitizenRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        AuditService.log(
            actor=user,
            action='insert',
            module='usuarios',
            target_model='usuarios',
            target_id=user.pk,
            description=f'Registro ciudadano: {user.correo}',
            request=request,
        )

        return Response(
            {
                **tokens,
                'tokens': tokens,
                'primary_role': user.get_primary_role(),
                'roles': user.get_role_codes(),
                'user': UserMeSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    AUTH-02: POST /api/v1/auth/login/ (y endpoint legacy /api/login/)
    Registra en plus.auditoria_accesos cada intento exitoso o fallido.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={200: AuthSessionResponseSerializer},
        summary='Inicio de sesión JWT + perfil de usuario (AUTH-02)',
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        attempted = (
            request.data.get('correo')
            or request.data.get('email')
            or request.data.get('username')
            or ''
        )
        if not serializer.is_valid():
            AuditService.log_access(
                actor=None,
                correo_intentado=attempted,
                tipo_evento='login',
                resultado='fallido',
                request=request,
            )
            serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        legacy_role = 'administrativo' if user.is_staff else 'cliente'

        AuditService.log_access(
            actor=user,
            correo_intentado=user.correo,
            tipo_evento='login',
            resultado='exitoso',
            request=request,
        )

        display_username = user.correo.split('@')[0] if user.correo.endswith('@plus.org') else user.correo
        return Response(
            {
                **tokens,
                'tokens': tokens,
                'usuario': display_username,
                'correo': user.correo,
                'rol': legacy_role,
                'primary_role': user.get_primary_role(),
                'roles': user.get_role_codes(),
                'user': UserMeSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """AUTH-04: POST /api/v1/auth/logout/ — Cierra sesión, revoca Token en servidor e invalida refresh."""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=inline_serializer(
            name='LogoutRequest',
            fields={
                'refresh': drf_serializers.CharField(
                    required=False,
                    help_text='Token JWT refresh opcional para invalidar.',
                ),
            },
        ),
        responses={
            200: inline_serializer(
                name='LogoutResponse',
                fields={
                    'message': drf_serializers.CharField(),
                    'detail': drf_serializers.CharField(),
                },
            )
        },
        summary='Cierre de sesión e invalidación de token en servidor (AUTH-04)',
    )
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        AuditService.log_access(
            actor=request.user,
            correo_intentado=request.user.correo,
            tipo_evento='logout',
            resultado='exitoso',
            request=request,
        )
        return Response(
            {'message': 'Sesión cerrada exitosamente.', 'detail': 'Sesión cerrada exitosamente.'},
            status=status.HTTP_200_OK,
        )


logger = logging.getLogger(__name__)


class PasswordResetRateThrottle(AnonRateThrottle):
    scope = 'password_reset'


class PasswordResetRequestView(APIView):
    """AUTH-05: POST /api/v1/auth/password-reset/request/"""
    permission_classes = [permissions.AllowAny]
    throttle_classes = [PasswordResetRateThrottle]
    serializer_class = PasswordResetRequestSerializer

    GENERIC_MESSAGE = (
        'Si el correo está asociado a una cuenta activa, recibirás instrucciones para restablecer tu contraseña.'
    )

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={
            200: inline_serializer(
                name='PasswordResetRequestResponse',
                fields={
                    'message': drf_serializers.CharField(),
                    'detail': drf_serializers.CharField(),
                },
            )
        },
        summary='Solicitar enlace de recuperación de contraseña por correo (AUTH-05)',
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        correo = serializer.validated_data['resolved_correo']

        cooldown = int(getattr(settings, 'PASSWORD_RESET_COOLDOWN_SECONDS', 60) or 0)
        cache_key = f'pwd_reset_cooldown:{correo}'
        if cooldown > 0 and cache.get(cache_key):
            return Response(
                {'message': self.GENERIC_MESSAGE, 'detail': self.GENERIC_MESSAGE},
                status=status.HTTP_200_OK,
            )

        user = User.objects.filter(correo__iexact=correo, estado=User.Estado.ACTIVO).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            try:
                send_password_reset_email(user, uid, token)
                if cooldown > 0:
                    cache.set(cache_key, True, timeout=cooldown)
                AuditService.log_access(
                    actor=user,
                    correo_intentado=correo,
                    tipo_evento='recuperacion_clave',
                    resultado='exitoso',
                    request=request,
                )
            except Exception as exc:
                logger.error(
                    'Fallo de envío SMTP en recuperación de contraseña para usuario=%s (%s)',
                    user.pk,
                    exc.__class__.__name__,
                )
                AuditService.log_access(
                    actor=user,
                    correo_intentado=correo,
                    tipo_evento='recuperacion_clave',
                    resultado='fallido',
                    request=request,
                )

        # Respuesta genérica sin revelar si el correo existe (regla AUTH-05)
        return Response(
            {'message': self.GENERIC_MESSAGE, 'detail': self.GENERIC_MESSAGE},
            status=status.HTTP_200_OK,
        )


class PasswordResetValidateView(APIView):
    """AUTH-06: POST /api/v1/auth/password-reset/validate/"""
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetValidateSerializer

    @extend_schema(
        request=PasswordResetValidateSerializer,
        responses={
            200: inline_serializer(
                name='PasswordResetValidateResponse',
                fields={'valid': drf_serializers.BooleanField()},
            )
        },
        summary='Validar enlace/token de recuperación sin cambiar la contraseña (AUTH-06)',
    )
    def post(self, request):
        serializer = PasswordResetValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['resolved_uid']))
            user = User.objects.get(pk=uid, estado=User.Estado.ACTIVO)
        except Exception:
            return Response(
                {'code': 'invalid_token', 'message': 'El enlace de recuperación es inválido o ha expirado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not default_token_generator.check_token(user, serializer.validated_data['resolved_token']):
            return Response(
                {'code': 'invalid_token', 'message': 'El enlace de recuperación es inválido o ha expirado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'valid': True}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """AUTH-07: POST /api/v1/auth/password-reset/confirm/"""
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={
            200: inline_serializer(
                name='PasswordResetConfirmResponse',
                fields={
                    'message': drf_serializers.CharField(),
                    'detail': drf_serializers.CharField(),
                },
            )
        },
        summary='Confirmar nueva contraseña, invalidar enlace y revocar sesiones anteriores (AUTH-07)',
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['resolved_uid']))
            user = User.objects.get(pk=uid, estado=User.Estado.ACTIVO)
        except Exception:
            return Response(
                {'code': 'invalid_token', 'message': 'El enlace de recuperación es inválido o ha expirado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not default_token_generator.check_token(user, serializer.validated_data['resolved_token']):
            return Response(
                {'code': 'invalid_token', 'message': 'El enlace de recuperación es inválido o ha expirado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_password = serializer.validated_data['new_password']
        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as exc:
            raise drf_serializers.ValidationError({'new_password': list(exc.messages)})

        AuditService.set_db_actor_session(user)
        user.set_password(new_password)
        user.save(update_fields=['password', 'fecha_actualizacion'])
        Token.objects.filter(user=user).delete()
        cache.delete(f'pwd_reset_cooldown:{user.correo.lower()}')
        AuditService.log_access(
            actor=user,
            correo_intentado=user.correo,
            tipo_evento='recuperacion_clave',
            resultado='exitoso',
            request=request,
        )
        return Response(
            {
                'message': 'Contraseña restablecida exitosamente.',
                'detail': 'Contraseña restablecida exitosamente.',
            },
            status=status.HTTP_200_OK,
        )


class MeProfileView(generics.RetrieveUpdateAPIView):
    """ME-01 y ME-02: GET / PATCH /api/v1/me/ (y /api/v1/auth/me/)"""
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        serializer.save()


class MePhotoView(APIView):
    """ME-03 y ME-04: PUT / POST / DELETE /api/v1/me/photo/"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    @extend_schema(
        request=inline_serializer(
            name='MePhotoUploadRequest',
            fields={
                'photo': drf_serializers.ImageField(
                    required=False,
                    help_text='Archivo de imagen (JPG, PNG o WEBP, máx. 15 MB). También acepta el nombre de campo `foto` o `file`.',
                ),
                'foto': drf_serializers.ImageField(required=False),
            },
        ),
        responses={200: UserProfileSerializer},
        summary='Subir o actualizar fotografía de perfil (ME-03)',
    )
    def post(self, request):
        return self.put(request)

    @extend_schema(
        request=inline_serializer(
            name='MePhotoPutRequest',
            fields={
                'photo': drf_serializers.ImageField(
                    required=False,
                    help_text='Archivo de imagen (JPG, PNG o WEBP, máx. 15 MB). También acepta el nombre de campo `foto` o `file`.',
                ),
                'foto': drf_serializers.ImageField(required=False),
            },
        ),
        responses={200: UserProfileSerializer},
        summary='Subir o actualizar fotografía de perfil (ME-03)',
    )
    def put(self, request):
        uploaded = request.FILES.get('photo') or request.FILES.get('foto') or request.FILES.get('file')
        if not uploaded:
            return Response(
                {'code': 'validation_error', 'message': 'Debe adjuntar un archivo de imagen en el campo photo/foto.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        validate_file_safety(uploaded)
        ext = os.path.splitext(uploaded.name)[1].lower()
        if ext not in ('.jpg', '.jpeg', '.png', '.webp'):
            return Response(
                {'code': 'validation_error', 'message': 'Solo se permiten fotografías en formato JPG, PNG o WEBP.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        saved_path = default_storage.save(f'profiles/{request.user.id}/avatar{ext}', uploaded)
        profile, _ = UserProfile.objects.get_or_create(usuario=request.user)
        profile.ruta_foto = f'/api/v1/public/media/{saved_path}'
        profile.save()
        return Response(UserProfileSerializer(profile).data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={204: None},
        summary='Eliminar fotografía de perfil (ME-04)',
    )
    def delete(self, request):
        profile, _ = UserProfile.objects.get_or_create(usuario=request.user)
        profile.ruta_foto = None
        profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MePreferencesView(generics.RetrieveUpdateAPIView):
    """ME-05: GET / PATCH /api/v1/me/preferences/"""
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        prefs, _ = UserPreference.objects.get_or_create(usuario=self.request.user)
        return prefs


class ChangePasswordView(APIView):
    """POST /api/v1/auth/change-password/"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        AuditService.set_db_actor_session(request.user)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password', 'fecha_actualizacion'])
        Token.objects.filter(user=request.user).delete()
        tokens = get_tokens_for_user(request.user)
        return Response(
            {
                'message': 'Contraseña actualizada exitosamente.',
                'tokens': tokens,
            },
            status=status.HTTP_200_OK,
        )


class ClienteProfileView(APIView):
    """GET /api/clientes/me/"""
    permission_classes = [IsClientOnly]
    serializer_class = UserMeSerializer

    def get(self, request):
        return Response(
            {
                'usuario': request.user.correo,
                'rol': 'cliente',
                'primary_role': request.user.get_primary_role(),
            },
            status=status.HTTP_200_OK,
        )


class AdministrativoProfileView(APIView):
    """GET /api/administrativos/me/"""
    permission_classes = [IsResponsibleOrAdmin]
    serializer_class = UserMeSerializer

    def get(self, request):
        return Response(
            {
                'usuario': request.user.correo,
                'rol': 'administrativo',
                'primary_role': request.user.get_primary_role(),
            },
            status=status.HTTP_200_OK,
        )


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    USR-01 a USR-06: Administración de usuarios (`plus.usuarios`), rol único y estado.
    """
    serializer_class = AdminUserCreateUpdateSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        qs = User.objects.select_related('rol').prefetch_related('asignaciones_ambito').all()
        params = self.request.query_params
        if id_rol := params.get('id_rol'):
            qs = qs.filter(rol_id=id_rol)
        elif role := (params.get('rol') or params.get('role')):
            qs = qs.filter(rol__nombre=normalize_role_name(role))
        if estado := params.get('estado'):
            qs = qs.filter(estado=estado.lower())
        if search := params.get('search'):
            qs = qs.filter(
                Q(correo__icontains=search)
                | Q(nombres__icontains=search)
                | Q(apellidos__icontains=search)
            )
        # USR-01: Filtro de elegibilidad de candidatos responsables para un caso específico
        if case_id := (params.get('eligible_for_case') or params.get('id_caso')):
            from apps.cases.models import Case
            case = Case.objects.filter(pk=case_id).first()
            if not case:
                # P10: Responder error explícito si el caso no existe en el filtro de candidatos
                raise ValidationError({'eligible_for_case': f'El caso con identificador "{case_id}" no existe.'})
            qs = qs.filter(
                estado=User.Estado.ACTIVO,
                rol__nombre__in=[Role.Nombre.REPRESENTANTE, Role.Nombre.ADMINISTRADOR],
            ).filter(
                Q(rol__nombre=Role.Nombre.ADMINISTRADOR)
                | Q(
                    asignaciones_ambito__activo=True,
                    asignaciones_ambito__comunidad_id=case.comunidad_id,
                )
                | Q(
                    asignaciones_ambito__activo=True,
                    asignaciones_ambito__tipo_caso_id=case.tipo_caso_id,
                )
            ).distinct()
        return qs

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        user = serializer.save()
        AuditService.log(
            actor=self.request.user,
            action='insert',
            module='usuarios',
            target_model='usuarios',
            target_id=user.pk,
            description=f'Creación administrativa de usuario {user.correo}',
            request=self.request,
        )

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        prev_user = serializer.instance
        prev_role_id = str(prev_user.rol_id) if prev_user.rol_id else None
        prev_estado = prev_user.estado
        user = serializer.save()

        # P16: Revocar sesión activa de inmediato ante cambio de rol o estado
        if (str(user.rol_id) != prev_role_id) or (user.estado != prev_estado):
            Token.objects.filter(user=user).delete()

        if str(user.rol_id) != prev_role_id:
            AuditService.log_permission_change(
                usuario_afectado=user,
                usuario_responsable=self.request.user,
                tipo_cambio='cambio_rol',
                valor_anterior={'id_rol': prev_role_id},
                valor_nuevo={'id_rol': str(user.rol_id)},
                motivo='Actualización administrativa de usuario',
                request=self.request,
            )

    def _apply_role_change(self, request, target_user):
        serializer = AssignUserRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_rol = serializer.validated_data.get('id_rol')
        raw_code = serializer.validated_data.get('role_code') or serializer.validated_data.get('rol') or ''

        if id_rol:
            new_role = generics.get_object_or_404(Role, pk=id_rol)
            target_role_name = new_role.nombre
        else:
            target_role_name = normalize_role_name(raw_code)
            new_role, _ = Role.objects.get_or_create(
                nombre=target_role_name,
                defaults={'descripcion': dict(Role.Nombre.choices).get(target_role_name, target_role_name)},
            )

        if (
            raw_code.upper() == 'SUPERADMIN' or target_role_name == Role.Nombre.ADMINISTRADOR
        ) and request.user.get_primary_role() != Role.Nombre.ADMINISTRADOR:
            return Response(
                {
                    'code': 'permission_denied',
                    'message': 'Solo un Administrador General puede otorgar el rol de administrador.',
                    'errors': {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # P15: Impedir cambio de rol si es el único administrador activo (last_admin_lock centralizado)
        if target_role_name != Role.Nombre.ADMINISTRADOR and target_user.is_last_active_admin:
            return Response(
                {
                    'code': 'last_admin_lock',
                    'message': 'No puedes revocar los permisos de administrador porque es el único administrador activo del sistema.',
                    'errors': {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        prev_role = target_user.rol
        role_changed = prev_role is None or prev_role.id != new_role.id

        AuditService.set_db_actor_session(request.user)
        target_user.rol = new_role
        target_user.save(update_fields=['rol', 'fecha_actualizacion'])

        # P16: Revocar sesiones activas del usuario afectado para forzar refresco y evitar navegación con rol desactualizado
        if role_changed:
            Token.objects.filter(user=target_user).delete()

        AuditService.log_permission_change(
            usuario_afectado=target_user,
            usuario_responsable=request.user,
            tipo_cambio='cambio_rol',
            valor_anterior={'id_rol': str(prev_role.id) if prev_role else None, 'nombre': prev_role.nombre if prev_role else ''},
            valor_nuevo={'id_rol': str(new_role.id), 'nombre': new_role.nombre},
            motivo=serializer.validated_data.get('motivo', ''),
            request=request,
        )

        id_comunidad = serializer.validated_data.get('id_comunidad')
        id_tipo_caso = serializer.validated_data.get('id_tipo_caso')
        if id_comunidad or id_tipo_caso:
            ResponsibleScopeAssignment.objects.create(
                usuario=target_user,
                comunidad_id=id_comunidad,
                tipo_caso_id=id_tipo_caso,
                activo=True,
            )

        return Response(UserMeSerializer(target_user).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=AssignUserRoleSerializer,
        responses={200: UserMeSerializer},
        summary='Asignar rol único al usuario (USR-05)',
    )
    @action(detail=True, methods=['put', 'post'], url_path='role')
    @transaction.atomic
    def change_single_role(self, request, pk=None):
        """USR-05: PUT /api/v1/admin/users/{id}/role/ — Asigna un único rol al usuario."""
        target_user = self.get_object()
        return self._apply_role_change(request, target_user)

    @extend_schema(
        request=AssignUserRoleSerializer,
        responses={200: UserMeSerializer},
        summary='Consultar o actualizar rol y ámbitos del usuario',
    )
    @action(detail=True, methods=['get', 'post', 'put'], url_path='roles')
    @transaction.atomic
    def manage_roles(self, request, pk=None):
        """Compatibilidad con /api/v1/admin/users/{id}/roles/"""
        target_user = self.get_object()
        if request.method == 'GET':
            return Response({
                'id_usuario': str(target_user.id),
                'rol': RoleSerializer(target_user.rol, context={'request': request}).data,
                'ambitos': ResponsibleScopeAssignmentSerializer(
                    target_user.asignaciones_ambito.all(), many=True
                ).data,
            })
        return self._apply_role_change(request, target_user)

    @extend_schema(
        request=AdminUserStatusSerializer,
        responses={200: UserMeSerializer},
        summary='Cambiar estado del usuario: activo, suspendido, inactivo (USR-06)',
    )
    @action(detail=True, methods=['patch'], url_path='status')
    @transaction.atomic
    def change_status(self, request, pk=None):
        """USR-06: PATCH /api/v1/admin/users/{id}/status/ — Cambia el estado (activo, suspendido, inactivo)."""
        target_user = self.get_object()
        serializer = AdminUserStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_estado = serializer.validated_data['estado']
        prev_estado = target_user.estado

        # P15: Impedir auto-desactivación o desactivar al único administrador activo (last_admin_lock centralizado)
        if new_estado != User.Estado.ACTIVO and target_user.is_last_active_admin:
            return Response(
                {
                    'code': 'last_admin_lock',
                    'message': 'No puedes suspender o desactivar la cuenta porque es el único administrador activo del sistema.',
                    'errors': {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        AuditService.set_db_actor_session(request.user)
        target_user.estado = new_estado
        target_user.save(update_fields=['estado', 'fecha_actualizacion'])

        # P16: Revocar sesiones activas ante cualquier cambio de estado
        Token.objects.filter(user=target_user).delete()

        AuditService.log(
            actor=request.user,
            action='update',
            module='usuarios',
            target_model='usuarios',
            target_id=target_user.pk,
            description=f'Cambio de estado de usuario {target_user.correo}: {prev_estado} -> {new_estado}',
            previous_data={'estado': prev_estado},
            new_data={'estado': new_estado, 'motivo': serializer.validated_data.get('motivo', '')},
            request=request,
        )
        return Response(UserMeSerializer(target_user).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """P15: Bloquear eliminación del último administrador activo."""
        target_user = self.get_object()
        if target_user.is_last_active_admin:
            return Response(
                {
                    'code': 'last_admin_lock',
                    'message': 'No puedes eliminar al único administrador activo del sistema.',
                    'errors': {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)


class AdminRoleViewSet(viewsets.ModelViewSet):
    """USR-07: GET /api/v1/admin/roles/"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAdminOrSuperAdmin()]
        return [IsSuperAdmin()]


class ResponsibleScopeAssignmentViewSet(viewsets.ModelViewSet):
    """Sección 14: GET/POST /api/v1/admin/responsibility-scopes/ y PATCH /api/v1/admin/responsibility-scopes/{id}/"""
    queryset = ResponsibleScopeAssignment.objects.select_related('usuario', 'comunidad', 'tipo_caso').all()
    serializer_class = ResponsibleScopeAssignmentSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        if uid := (params.get('id_usuario') or params.get('usuario')):
            qs = qs.filter(usuario_id=uid)
        if cid := params.get('id_comunidad'):
            qs = qs.filter(comunidad_id=cid)
        if tid := params.get('id_tipo_caso'):
            qs = qs.filter(tipo_caso_id=tid)
        if activo := params.get('activo'):
            qs = qs.filter(activo=activo.lower() in ('true', '1'))
        return qs

    def perform_create(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        serializer.save()

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        serializer.save()
