from django.urls import path
from . import views

urlpatterns = [
    path('', views.finance),
    path('finance/', views.finance_list),
    path('finance/<int:id>/', views.finance_detail)
]