# Account_Module/permissions.py
from rest_framework import permissions
from rest_framework.permissions import BasePermission
class user_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='user-model-manager').exists()
    
class usergroup_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='usergroup-model-manager').exists()
    

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
    
class peyment_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='peyment-model-manager').exists()
    
class order_manager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='order-model-manager').exists()


    #access_all-model-manager
	#access_by_user-model-manager
	#access_by_usergroup-model-manager
	#category-model-manager
	#order-model-manager
	#peyment-model-manager
	#procuct-model-manager
	#user-model-manager
	#usergroup-model-manager