from rest_framework import serializers
from .models import Task, Category


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        
        validated_data.pop('user', None)
        return Task.objects.create(user=user, **validated_data)

    """ def create(self, validated_data):
        
        Create and return a new `Snippet` instance, given the validated data.
        
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
        Update and return an existing `Snippet` instance, given the validated data.
        
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance """
    
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        
        validated_data.pop('user', None)
        return Category.objects.create(user=user, **validated_data)