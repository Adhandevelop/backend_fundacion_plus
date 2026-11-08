from rest_framework.permissions import BasePermission
from apps.accounts.models import Role


class IsCitizen(BasePermission):
    """Permite acceso a cualquier usuario autenticado y activo (ciudadano, representante, moderador, administrador)."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active)


class IsClientOnly(BasePermission):
    """Permiso compatible con endpoint legacy /api/clientes/me/ (solo rol ciudadano)."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.get_primary_role() == Role.Nombre.CIUDADANO
        )


class IsResponsibleOrAdmin(BasePermission):
    """Permite acceso a representante, moderador o administrador."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.has_any_role(
                Role.Nombre.REPRESENTANTE,
                Role.Nombre.MODERADOR,
                Role.Nombre.ADMINISTRADOR,
            )
        )


class IsEditorOrAdmin(BasePermission):
    """Permite acceso a moderador/editor o administrador."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.has_any_role(
                Role.Nombre.MODERADOR,
                Role.Nombre.ADMINISTRADOR,
            )
        )


class IsAdminOrSuperAdmin(BasePermission):
    """Permite acceso a administrador o moderador en funciones administrativas."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR)
        )


class IsSuperAdmin(BasePermission):
    """Permite acceso exclusivamente al rol administrador general de PLUS."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.get_primary_role() == Role.Nombre.ADMINISTRADOR
        )
