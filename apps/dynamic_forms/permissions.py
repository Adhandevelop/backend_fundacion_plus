from rest_framework import permissions
from apps.accounts.models import Role


class CanManageForms(permissions.BasePermission):
    """
    Permite acceso exclusivamente a usuarios con rol administrador y capacidad can_manage_forms.
    Moderadores, representantes y ciudadanos reciben 403 Forbidden.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.get_primary_role() == Role.Nombre.ADMINISTRADOR
            and getattr(user, 'can_manage_forms', False)
        )
