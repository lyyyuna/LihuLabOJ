from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow Admin users to edit it.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Write/Upgrade/Delete permissions are only allowed to Admin users.
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and
            permissions.is_authenticated(request.user) and
            request.user.is_staff
        )