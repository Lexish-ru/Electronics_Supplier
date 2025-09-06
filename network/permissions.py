from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """
    Доступ только для активных сотрудников (is_active и is_staff).
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)