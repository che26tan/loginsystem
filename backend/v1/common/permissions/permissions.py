from rest_framework import permissions


class IsVisitorPermission(permissions.IsAdminUser):
    pass

class IsOwnerPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class IsStaffPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.apiuser == request.user.id

class IsManagerPermission(permissions.BasePermission):
    pass