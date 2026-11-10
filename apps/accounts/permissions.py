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
    """Permite acceso a representante territorial, moderador o administrador."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and (
                user.is_superuser
                or user.has_any_role(
                    Role.Nombre.REPRESENTANTE,
                    Role.Nombre.MODERADOR,
                    Role.Nombre.ADMINISTRADOR,
                )
            )
        )


class IsRepresentativeOrAdmin(BasePermission):
    """Permite acceso a representante territorial o administrador."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and (
                user.is_superuser
                or user.has_any_role(
                    Role.Nombre.REPRESENTANTE,
                    Role.Nombre.ADMINISTRADOR,
                )
            )
        )


class IsModeratorOrAdmin(BasePermission):
    """Permite acceso a moderador o administrador (p. ej. moderación de casos y comentarios)."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and (
                user.is_superuser
                or user.has_any_role(
                    Role.Nombre.MODERADOR,
                    Role.Nombre.ADMINISTRADOR,
                )
            )
        )


class IsEditorOrAdmin(IsModeratorOrAdmin):
    """Permite acceso a moderador/editor o administrador."""
    pass


class IsAdminOrSuperAdmin(BasePermission):
    """Permite acceso exclusivamente al rol administrador general de PLUS o superusuario de Django."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and (
                user.is_superuser
                or user.get_primary_role() == Role.Nombre.ADMINISTRADOR
            )
        )


IsAdminUser = IsAdminOrSuperAdmin
IsAdminOnly = IsAdminOrSuperAdmin


class IsSuperAdmin(IsAdminOrSuperAdmin):
    """Permite acceso exclusivamente al rol administrador general de PLUS."""
    pass
