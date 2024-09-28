from django.shortcuts import get_object_or_404, render
from rest_framework import status
from .serializers import TaskSerializer, CategorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound

@extend_schema(
    request=TaskSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request):

    task = TaskSerializer(data=request.data, context={'request': request})

    print(task)

    if task.is_valid():
        task.save(user=request.user) 
        return Response(task.data, status=status.HTTP_201_CREATED)
    else:
        print(task.errors)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_tasks(request):
     
    if request.query_params:
        tasks = Task.objects.filter(**request.query_params.dict(), user = request.user)
    else:
        tasks = Task.objects.filter(user = request.user)
 
    if tasks:
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_task(request, pk):

    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        raise NotFound(detail="Task not found.")

    task = Task.objects.filter(user = request.user, pk=pk)
 
    if task:
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    request=TaskSerializer
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, pk):

    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        raise NotFound(detail="Task not found.")

    data = TaskSerializer(instance=task, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        print(data.errors)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_categories(request):
     
    if request.query_params:
        categories = Category.objects.filter(**request.query_params.dict(), user = request.user)
    else:
        categories = Category.objects.filter(user = request.user)
 
    if categories:
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    request=CategorySerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category(request):

    category = CategorySerializer(data=request.data, context={'request': request})

    if category.is_valid():
        category.save(user=request.user) 
        return Response(category.data, status=status.HTTP_201_CREATED)
    else:
        print(category.errors)
        return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    request=CategorySerializer
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_category(request, pk):

    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound(detail="Category not found.")

    data = CategorySerializer(instance=category, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        print(data.errors)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return Response(status=status.HTTP_202_ACCEPTED)