from rest_framework.permissions import BasePermission
from apps.accounts.models import Role


class IsCitizen(BasePermission):
    """Permite acceso a cualquier usuario autenticado y activo (ciudadano, representante, moderador, administrador)."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active)


class IsClientOnly(BasePermission):
    """Permiso exclusivo para el rol ciudadano (P01: endpoints exclusivamente ciudadanos)."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.get_primary_role() == Role.Nombre.CIUDADANO
        )


IsCitizenOnly = IsClientOnly


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


class IsSuperAdmin(BasePermission):
    """
    Permite acceso exclusivamente a cuentas con capacidad de superadministrador de PLUS
    (rol administrador y privilegio persistente can_manage_homepage).
    Los administradores estándar reciben 403 Forbidden.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.get_primary_role() == Role.Nombre.ADMINISTRADOR
            and getattr(user, 'can_manage_homepage', False)
        )
