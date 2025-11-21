from rest_framework import permissions
from rest_framework.permissions import BasePermission


class config_price_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='config_price_manage-model-manager').exists()

class access_all_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='access_all-model-manager').exists()
    


class access_by_user_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='access_by_user-model-manager').exists()


class access_by_usergroup_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='access_by_usergroup-model-manager').exists()