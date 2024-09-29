from django.db import models
from core.models import User

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    isPinned = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    tags = models.ManyToManyField('Tag', related_name='notes', blank=True)

    def __str__(self) -> str:
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self) -> str:
        return self.name