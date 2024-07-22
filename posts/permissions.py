from rest_framework import permissions

class IsPostOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        
        return obj.user == request.user or request.user.is_staff
