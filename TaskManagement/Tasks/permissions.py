from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

'''
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'
    
class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'member'
'''

class CanComment(BasePermission):
    """
    Admin: any project
    Manager: only projects they created or are a member of
    Member: only tasks assigned to them
    """
    def has_object_permission(self, request, view, obj):
        # obj = Task instance
        user = request.user
        role = user.role
        project = obj.project

        if role == 'admin':
            return True

        if role == 'manager':
            return (
                project.created_by == user or
                project.members.filter(id=user.id).exists()
            )

        if role == 'member':
            return obj.assigned_to.filter(id=user.id).exists()

        return False
    
class CanAccessTask(BasePermission):
    """
    Admin: any task
    Manager: only tasks in projects they created or are a member of
    Member: only tasks assigned to them
    """
    def has_object_permission(self, request, view, obj):
        # obj = Task instance
        user = request.user
        role = user.role
        project = obj.project

        if role == 'admin':
            return True

        if role == 'manager':
            return (
                project.created_by == user or
                project.members.filter(id=user.id).exists()
            )

        if role == 'member':
            return obj.assigned_to.filter(id=user.id).exists()

        return False


class IsProjectOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj = Project instance
        return request.user.is_authenticated and (
            request.user.role == 'admin' or
            obj.created_by == request.user
        )    

