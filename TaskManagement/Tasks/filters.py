import django_filters
from django.db.models import Q
from .models import Project, Task, Comment


class ProjectFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('status', 'status'),
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('created_by','created_by'))
            )
    class Meta:
        model = Project
        fields = {
            'name': ['icontains'],
            'status': ['exact'],
            'created_at': ['gte', 'lte'],
            'created_by': ['exact'],
            'updated_at': ['gte', 'lte'],
        }
    def filter_search(self, queryset, name, value):
        # Case-insensitive search across name OR status
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value) | Q(status__icontains=value)
        )


class TaskFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('due_date', 'due_date'),
            ('priority', 'priority'),
            ('status', 'status'),
            ('created_at', 'created_at'),
            ('created_by','created_by'))
            )
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
    def filter_search(self, queryset, name, value):
        # Case-insensitive search across name OR status
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value) | Q(status__icontains=value) | Q(priority__icontains=value)
        )


class CommentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('task','task'),
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('author', 'author'))
            )
    class Meta:
        model = Comment
        fields = {
            'task': ['exact'],
            'author': ['exact'],
            'created_at': ['gte', 'lte'],
            'updated_at': ['gte', 'lte'],
        }
    def filter_search(self, queryset, name, value):
        # Case-insensitive search across name OR status
        return queryset.filter(
            Q(content__icontains=value) | Q(author__username__icontains=value)
        )

