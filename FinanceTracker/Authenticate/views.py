from .serializer import SignupSerializer 
from rest_framework.response import Response 
from rest_framework.decorators import api_view  
from django.http import HttpResponse 
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

user = get_user_model()

# Create your views here.
# 'GET' method is used to retrieve data 
# 'POST' method is used to create/modify data

@api_view(['POST' , 'GET'])
def SignupView(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'})
        return Response(serializer.errors)
    elif request.method == 'GET':
        return Response({'message': 'Signup View'})

@api_view(['POST' , 'GET'])
def LoginView(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        print(f"Authenticated user: {user}") # Debugging statement to check the authenticated user
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful', 'token': token.key})
        else:
            return Response({'message': 'Invalid credentials'})
    elif request.method == 'GET':
        return Response({'message': 'Login View'})

def authenticate_user(request):
    return HttpResponse("Authenticate User")