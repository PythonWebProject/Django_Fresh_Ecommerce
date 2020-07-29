from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    '''对象级别的权限，仅允许对象的所有者对其进行编辑'''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user