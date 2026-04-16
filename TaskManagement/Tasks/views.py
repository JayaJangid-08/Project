from urllib import request

from django.http import HttpResponse
from django.tasks import task
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from .models import Task , Project , Comment
from Authenticate.models import User
from .permissions import IsAdmin , CanComment , IsProjectOwnerOrAdmin , CanAccessTask
# from .permissions import

# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Task Management System")


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def project_list(request):
    if request.method == 'GET':
        if request.user.role =='admin':
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(created_by=request.user)

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        permission = IsProjectOwnerOrAdmin()
        if not permission.has_permission(request , None):
            return Response({'message': 'Permission denied'})
        
        print(f"Request data: {request.data}")
        serializer = ProjectSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        
        return Response(serializer.errors)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def project_detail(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'message': 'Project not found'})
    
    is_admin = IsAdmin()
    if not is_admin.has_permission(request , None):
        if request.user not in project.members.all() and request.user != project.created_by:
            return Response({'message': 'Access denied'})

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        permission = IsProjectOwnerOrAdmin()
        if not permission.has_object_permission(request , None):
            return Response({'message': 'Permission denied'})
        
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        permission = IsAdmin()
        if permission.has_permission(request , None):
            return Response({'message' : 'Only admin can delete projects.'})
        project.delete()
        return Response({'message': 'Project deleted successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'message': 'Project not found'})
    
    # only creator can add members
    permission = IsProjectOwnerOrAdmin()
    if not permission.has_object_permission(request , None):
        return Response({'message': 'Access denied'})
    
    try:
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'message': 'User not found'})
    
    # already member check
    if user in project.members.all():
        return Response({'message': 'User is already a member'})
    
    project.members.add(user)
    return Response({'message': 'Member added successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_member(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'message': 'Project not found'})
    
    # only creator can remove members
    permission = IsProjectOwnerOrAdmin()
    if request.user != project.created_by or not permission.has_permission(request , None , project) :
        return Response({'message': 'Access denied'})
    
    try:
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'message': 'User not found'})
    
    if user not in project.member.all():
        return Response({'message' : 'User is not a member of this project.'})

    project.members.remove(user)
    return Response({'message': 'Member removed successfully'})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'message': 'Project not found'})

    if request.method == 'GET':
        role = request.user.role
        if role == 'admin':
            tasks = Task.objects.filter(project=project)
        elif role == 'manager':
            # Manager can only see tasks in projects they created
            if project.created_by != request.user:
                return Response({'message': 'Access denied'})
            tasks = Task.objects.filter(project=project)
        else:
            # Member sees only their own assigned tasks
            tasks = Task.objects.filter(project=project, assigned_to=request.user)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Only admin and manager can create tasks
        permission = IsProjectOwnerOrAdmin()
        if not permission.has_permission(request, None):
            return Response({'message': 'Only admin or manager can create tasks'})

        # Manager can only create tasks in their own projects
        project_permission = IsProjectOwnerOrAdmin()
        if not project_permission.has_object_permission(request, None, project):
            return Response({'message': 'Managers can only create tasks in their own projects'})

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, project=project)
            return Response(serializer.data)

        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, project_id, task_id):
    try:
        task = Task.objects.select_related('project').get(id=task_id, project_id=project_id)
    except Task.DoesNotExist:
        return Response({'message': 'Task not found'})

    # Gate all methods through CanAccessTask first
    access = CanAccessTask()
    if not access.has_object_permission(request, None, task):
        return Response({'message': 'Access denied'})

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'DELETE':
        # Only admin can delete tasks
        permission = IsAdmin()
        if not permission.has_permission(request, None):
            return Response({'message': 'Only admin can delete tasks'})

        task.delete()
        return Response({'message': 'Task deleted successfully'})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list(request, project_id, task_id):
    try:
        task = Task.objects.select_related('project').get(id=task_id, project_id=project_id)
    except Task.DoesNotExist:
        return Response({'message': 'Task not found'})

    permission = CanComment()
    if not permission.has_object_permission(request, None, task):
        return Response({'message': 'Access denied'})

    if request.method == 'GET':
        comments = Comment.objects.filter(task=task).select_related('author')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        content = request.data.get('content')
        if not content:
            return Response({'message' : 'Content required.'})
        
        comment = Comment.objects.create(task=task, author=request.user, content=content)
        return Response({'message': 'Comment added', 'id': comment.id})


