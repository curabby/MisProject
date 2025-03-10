from apps.core.models import Users
from rest_framework import permissions


def role_compliance_check(user: Users, role_name: str) -> bool:
    return bool(user.is_authenticated and user.role.name == role_name)


class IsDoctor(permissions.BasePermission):
    """
    Доступ только аутентифицированным пользователям с ролью 'doctor'.
    """
    def has_permission(self, request, view):
        return role_compliance_check(request.user, 'doctor')


class IsAdmin(permissions.BasePermission):
    """
    Доступ только аутентифицированным пользователям с ролью 'admin'.
    """
    def has_permission(self, request, view):
        return role_compliance_check(request.user, 'admin')


class IsPatient(permissions.BasePermission):
    """
    Доступ только аутентифицированным пользователям с ролью 'patient'.
    """
    def has_permission(self, request, view):
        return role_compliance_check(request.user, 'patient')
