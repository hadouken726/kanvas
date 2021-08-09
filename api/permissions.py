from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    

class ReadOnlyCourses(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True