import django_filters
from .models import Project, Task, Comment

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = {
            'name': ['icontains'],
            'status': ['exact'],
            'created_at': ['gte', 'lte'],
            'created_by': ['exact'],
            'updated_at': ['gte', 'lte'],
        }

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'title': ['icontains'],
            'project': ['exact'],
            'status': ['exact'],
            'priority': ['exact'],
            'created_at': ['gte', 'lte'],
            'created_by': ['exact'],
        }

class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = {
            'task': ['exact'],
            'author': ['exact'],
            'created_by': ['exact'],
            'updated_at': ['gte', 'lte'],
        }