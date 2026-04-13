from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('project/<int:id>/', views.task_detail, name='task_detail'),
    path('project/<int:id>/add-member/', views.add_member, name='add_member'),
    path('project/<int:id>/remove-member/', views.remove_member, name='remove_member'),
    path('project/<int:id>/update-status/', views.update_status, name='update_status'),
    path('project/<int:id>/priority/', views.update_priority, name='update_priority'),
]