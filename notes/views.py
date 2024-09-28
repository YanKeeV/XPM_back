from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from .serializers import NoteSerializer, TagSerializer
from .models import Note, Tag

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_notes(request):
     
    if request.query_params:
        notes = Note.objects.filter(**request.query_params.dict(), user = request.user)
    else:
        notes = Note.objects.filter(user = request.user)
 
    if notes:
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_note(request, pk):

    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        raise NotFound(detail="Note not found.")

    note = Note.objects.filter(user = request.user, pk=pk)
 
    if note:
        serializer = NoteSerializer(note, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    request=NoteSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_note(request, *args, **kwargs):

    tags_data = request.data.pop('tags', [])

    serializer = NoteSerializer(data=request.data)
    
    print('Tags:', tags_data)

    if serializer.is_valid():

        note = serializer.save(user=request.user)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults={
                    'color': tag_data.get('color', ''),
                    'user': request.user
                }
            )
            note.tags.add(tag)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=NoteSerializer
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, pk, *args, **kwargs):
    try:
        note = Note.objects.get(id=pk, user=request.user)
    except Note.DoesNotExist:
        return Response({"error": "Note not found or you do not have permission to update this note."}, status=status.HTTP_404_NOT_FOUND)

    tags_data = request.data.pop('tags', [])

    serializer = NoteSerializer(note, data=request.data, partial=True)

    if serializer.is_valid():

        note = serializer.save()

        current_tags = set(note.tags.all())
        new_tags = set()

        for tag_data in tags_data:

            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults={
                    'color': tag_data.get('color', ''),
                    'user': request.user  
                }
            )
            new_tags.add(tag)

            if tag not in current_tags:
                note.tags.add(tag)

        tags_to_remove = current_tags - new_tags
        for tag in tags_to_remove:
            note.tags.remove(tag)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note(request, pk):
    try:
        note = Note.objects.get(id=pk, user=request.user)

        tags = list(note.tags.all())

        note.delete()

        for tag in tags:
            if tag.notes.count() == 0:
                tag.delete()

        return Response({"message": "Note and unused tags deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    except Note.DoesNotExist:
        return Response({"error": "Note not found or you do not have permission to delete this note."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_tags(request):
     
    if request.query_params:
        tags = Tag.objects.filter(**request.query_params.dict(), user = request.user)
    else:
        tags = Tag.objects.filter(user = request.user)
 
    if tags:
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@extend_schema(
    request=TagSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_tag(request):

    tag = TagSerializer(data=request.data, context={'request': request})

    if tag.is_valid():
        tag.save(user=request.user) 
        return Response(tag.data, status=status.HTTP_201_CREATED)
    else:
        print(tag.errors)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@extend_schema(
    request=TagSerializer
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_tag(request, pk):

    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        raise NotFound(detail="Tag not found.")

    data = TagSerializer(instance=tag, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        print(data.errors)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    return Response(status=status.HTTP_202_ACCEPTED)