from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Finance
from .serializer import FinanceSerializer
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def finance(request):
    return HttpResponse("Finance Tracker Application.")

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def finance_list(request):
    print(f"User: {request.user}")
    if request.method == 'GET':
        finance = Finance.objects.filter(created_by=request.user)
        serializer = FinanceSerializer(finance, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print(f"Request data: {request.data}")
        serializer = FinanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def finance_detail(request, id):
    try:
        finance = Finance.objects.get(id=id, created_by=request.user)
    except Finance.DoesNotExist:
        return Response({'message': 'Finance not found'})
    
    if request.method == 'GET':
        serializer = FinanceSerializer(finance)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = FinanceSerializer(finance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        finance.soft_delete()
        return Response({'message': 'Finance deleted successfully'})


