from rest_framework import permissions
from rest_framework.permissions import BasePermission


class order_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='order-model-manager').exists()