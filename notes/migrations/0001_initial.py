# Generated by Django 4.2.4 on 2024-09-28 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('isPinned', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='NoteToTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.note')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.tag')),
            ],
        ),
    ]
