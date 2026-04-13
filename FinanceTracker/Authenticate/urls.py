from django.urls import path
from . import views


urlpatterns = [
    path('', views.authenticate_user),
    path('signup/', views.SignupView),
    path('login/', views.LoginView)
]
