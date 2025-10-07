from rest_framework import viewsets, permissions
from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of a post or comment
    to edit or delete it.
    """

    
    def has_object_permission(self, request, view, obj):
        
        # SAFE_METHODS = GET, HEAD, OPTIONS (read-only access)
        if request.method in permissions.SAFE_METHODS:
        # instead of typing: if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Only allow owners to modify or delete
        return obj.author == request.user