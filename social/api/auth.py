from rest_framework import permissions

from settings.models import Settings
from node.models import Node


class APIAuthentication(permissions.BasePermission):

    def has_permission(self, request, view):
        settings = Settings.objects.first()
        if not settings.auth_required:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        try:
            Node.objects.get(user=user)
        except Node.DoesNotExist:
            return False
        return True
