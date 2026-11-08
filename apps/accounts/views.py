from django.db import transaction
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import (
    ResponsibleScopeAssignment,
    Role,
    User,
    normalize_role_name,
)
from apps.accounts.permissions import (
    IsAdminOrSuperAdmin,
    IsClientOnly,
    IsSuperAdmin,
)
from apps.accounts.serializers import (
    AdminUserCreateUpdateSerializer,
    AssignUserRoleSerializer,
    ChangePasswordSerializer,
    CitizenRegistrationSerializer,
    LoginSerializer,
    ResponsibleScopeAssignmentSerializer,
    RoleSerializer,
    UserMeSerializer,
)
from apps.audit.services import AuditService


def get_tokens_for_user(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    refresh['correo'] = user.correo
    refresh['roles'] = user.get_role_codes()
    refresh['primary_role'] = user.get_primary_role()
    token_obj, _ = Token.objects.get_or_create(user=user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'token': token_obj.key,
    }


class CitizenRegisterView(APIView):
    """POST /api/v1/auth/register/ — Registro ciudadano en plus.usuarios."""
    permission_classes = [permissions.AllowAny]
    serializer_class = CitizenRegistrationSerializer

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
                'user': UserMeSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST /api/v1/auth/login/ (y endpoint legacy /api/login/)
    Registra en plus.auditoria_accesos cada intento exitoso o fallido.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

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
                'usuario': display_username,
                'correo': user.correo,
                'rol': legacy_role,
                'primary_role': user.get_primary_role(),
                'roles': user.get_role_codes(),
                'user': UserMeSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class MeProfileView(generics.RetrieveUpdateAPIView):
    """GET / PATCH /api/v1/auth/me/"""
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


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
        return Response({'message': 'Contraseña actualizada exitosamente.'}, status=status.HTTP_200_OK)


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
    permission_classes = [IsAdminOrSuperAdmin]
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
    Administración de usuarios (`plus.usuarios`) y ámbitos de responsables (`plus.asignaciones_responsables`).
    """
    serializer_class = AdminUserCreateUpdateSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        qs = User.objects.select_related('rol').prefetch_related('asignaciones_ambito').all()
        params = self.request.query_params
        if role := (params.get('rol') or params.get('role')):
            qs = qs.filter(rol__nombre=normalize_role_name(role))
        if estado := params.get('estado'):
            qs = qs.filter(estado=estado.lower())
        if search := params.get('search'):
            qs = (
                qs.filter(correo__icontains=search)
                | qs.filter(nombres__icontains=search)
                | qs.filter(apellidos__icontains=search)
            )
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
        prev_role_id = str(serializer.instance.rol_id)
        user = serializer.save()
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

    @action(detail=True, methods=['get', 'post'], url_path='roles')
    @transaction.atomic
    def manage_roles(self, request, pk=None):
        """
        GET / POST /api/v1/admin/users/{id}/roles/
        Cambia el rol en `plus.usuarios`, registra en `plus.auditoria_permisos` y opcionalmente
        crea una asignación en `plus.asignaciones_responsables`.
        """
        target_user = self.get_object()
        if request.method == 'GET':
            return Response({
                'id_usuario': str(target_user.id),
                'rol': RoleSerializer(target_user.rol).data,
                'ambitos': ResponsibleScopeAssignmentSerializer(
                    target_user.asignaciones_ambito.all(), many=True
                ).data,
            })

        serializer = AssignUserRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw_code = serializer.validated_data['role_code']
        target_role_name = normalize_role_name(raw_code)

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

        prev_role = target_user.rol
        new_role, _ = Role.objects.get_or_create(
            nombre=target_role_name,
            defaults={'descripcion': dict(Role.Nombre.choices).get(target_role_name, target_role_name)},
        )

        AuditService.set_db_actor_session(request.user)
        target_user.rol = new_role
        target_user.save(update_fields=['rol', 'fecha_actualizacion'])

        AuditService.log_permission_change(
            usuario_afectado=target_user,
            usuario_responsable=request.user,
            tipo_cambio='cambio_rol',
            valor_anterior={'id_rol': str(prev_role.id), 'nombre': prev_role.nombre},
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


class AdminRoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAdminOrSuperAdmin()]
        return [IsSuperAdmin()]
