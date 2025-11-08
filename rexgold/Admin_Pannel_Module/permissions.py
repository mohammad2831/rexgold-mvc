# Account_Module/permissions.py
from rest_framework import permissions

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            getattr(request.user, 'user_status', None) == 'employee'
        )