from rest_framework import permissions

from social.settings import API_AUTH_REQUIRED
from node.models import Node


class APIAuthentication(permissions.BasePermission):

    def has_permission(self, request, view):
        if not API_AUTH_REQUIRED:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        try:
            Node.objects.get(user=user)
        except Node.DoesNotExist:
            return False
        return True
