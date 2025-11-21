from rest_framework import permissions
from rest_framework.permissions import BasePermission


class product_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='product-model-manager').exists()
    

class category_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='catgory-model-manager').exists()
    
