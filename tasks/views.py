from django.shortcuts import get_object_or_404, render
from rest_framework import status
from .serializers import TaskSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task
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

    task = Task.objects.get(pk=pk)
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