from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Projects
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/members/add/', views.add_member, name='add_member'),
    path('projects/<int:project_id>/members/remove/', views.remove_member, name='remove_member'),

    # Tasks
    # It'll print all the tasks available in that particular 'project_id'
    path('projects/<int:project_id>/tasks/', views.task_list, name='task_list'), 
    # It'll print specific task available in that particular 'project_id' and 'task_id'
    path('projects/<int:project_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),

    # Comments
    path('projects/<int:project_id>/tasks/<int:task_id>/comments/', views.comment_list, name='comment_list'),
]


