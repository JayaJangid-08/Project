from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from .models import Task , Project , Comment
from Authenticate.models import User
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
        if request.user.role not in ['admin', 'manager']:
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
    
    if request.user not in project.members.all() and request.user != project.created_by:
        return Response({'message': 'Access denied'})

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if request.user.role not in ['admin', 'manager']:
            return Response({'message': 'Permission denied'})
        
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    # elif request.method == 'DELETE':
    #     project.delete()
    #     return Response({'message': 'Project deleted successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'message': 'Project not found'})
    
    # only creator can add members
    if request.user != project.created_by :
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
    if request.user != project.created_by:
        return Response({'message': 'Access denied'})
    
    try:
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'message': 'User not found'})
    
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
        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if request.user.role not in ['admin', 'manager']:
            return Response({'message': 'Only admin and manager can create tasks'})

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, project=project)
            return Response(serializer.data)
        
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, project_id, task_id):
    try:
        task = Task.objects.get(id=task_id, project_id=project_id)
    except Task.DoesNotExist:
        return Response({'message': 'Task not found'})

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # member can only update status and priority
        if request.user != task.assigned_to and request.user.role not in ['admin', 'manager']:
            return Response({'message': 'Access denied'})

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        if request.user.role != 'admin':
            return Response({'message': 'Only admin can delete task'})
        
        task.delete()
        return Response({'message': 'Task deleted successfully'})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list(request, project_id, task_id):
    try:
        task = Task.objects.select_related('project').get(id=task_id, project_id=project_id)
    except Task.DoesNotExist:
        return Response({'message': 'Task not found'}, status=404)

    if request.method == 'GET':
        comments = Comment.objects.filter(task=task).select_related('author')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = request.user
        role = user.role
        project = task.project

        is_admin = role == 'admin'
        is_manager = role == 'manager' and (
            project.created_by == user or
            project.members.filter(id=user.id).exists()
        )
        is_assigned = task.assigned_to.filter(id=user.id).exists()

        if is_admin or is_manager or is_assigned:
            content = request.data.get('content')
            if not content:
                return Response({'message': 'Content required'})
            comment = Comment.objects.create(task=task, author=user, content=content)
            return Response({'message': 'Comment added', 'id': comment.id})

    return Response({'message': 'Access denied'})