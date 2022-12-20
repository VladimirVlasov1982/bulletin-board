from rest_framework.permissions import BasePermission
from users.models import User, UserRoles


class IsOwnerOrAdmin(BasePermission):
    message = "Вы не являетесь владельцем или администратором"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.role == UserRoles.ADMIN:
            return True
        return False
