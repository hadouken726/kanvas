from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        if view.__class__.__name__ == 'SubmissionView':
            if request.method == 'PUT' or request.method == 'GET':
                return request.user.is_superuser
            else:
                return False
        return request.user.is_superuser

class ReadOnlyCourses(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True


class IsFacilitator(BasePermission):
    def has_permission(self, request, view):
        if view.__class__.__name__ == 'SubmissionView':
            if request.method == 'PUT' or request.method == 'GET':
                return request.user.is_staff and not request.user.is_superuser
            else:
                return False
        return request.user.is_staff and not request.user.is_superuser

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if view.__class__.__name__ == 'SubmissionView':
            if request.method == 'POST' or request.method == 'GET':
                return not request.user.is_staff and not request.user.is_superuser
            else:
                return False
        return not request.user.is_staff and not request.user.is_superuser