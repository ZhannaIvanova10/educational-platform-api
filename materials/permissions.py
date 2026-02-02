from rest_framework import permissions
from django.contrib.auth.models import Group


class IsModerator(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModerator(permissions.BasePermission):
    """Разрешает доступ владельцу или модератору"""

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Проверяем, является ли пользователь модератором
        is_moderator = request.user.groups.filter(name='moderators').exists()
        # Проверяем, является ли пользователь владельцем
        is_owner = obj.owner == request.user

        return is_moderator or is_owner


class IsNotModerator(permissions.BasePermission):
    """Проверяет, что пользователь НЕ модератор"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return not request.user.groups.filter(name='moderators').exists()