from rest_framework import serializers
from .models import Note, Tag
    
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        
        validated_data.pop('user', None)
        return Tag.objects.create(user=user, **validated_data)
    
class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'createdAt', 'isPinned', 'user', 'tags']
        read_only_fields = ['id', 'createdAt']
        
    def create(self, validated_data):

        user = validated_data.pop('user')
        note = Note.objects.create(user=user, **validated_data)

        return note