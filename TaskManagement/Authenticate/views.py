from contextvars import Token
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import SignupSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Task Management Application.")

@api_view(['GET', 'POST'])
def Signup(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'})
        return Response(serializer.errors)
    elif request.method == 'GET':
        return Response({'message': 'Signup View'})

@api_view(['GET', 'POST'])
def Login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        print(f"Authenticated user: {user}") # Debugging statement to check the authenticated user
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response({'message': 'Login successful', 'access': str(access), 'refresh': str(refresh)})
        else:
            return Response({'message': 'Invalid credentials'})
    elif request.method == 'GET':
        return Response({'message': 'Login View'})

