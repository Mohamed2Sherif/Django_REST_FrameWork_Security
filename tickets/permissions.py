from rest_framework import permissions


class is_allowed_author(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        return obj.Author == request.user