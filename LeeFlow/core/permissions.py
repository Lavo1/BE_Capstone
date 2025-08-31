from rest_framework import permissions

class IsPartnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Admin', 'Partner']

class IsSecretary(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Secretary'

class CanEditTimeEntry(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Secretary':
            return obj.user == request.user
        return True
