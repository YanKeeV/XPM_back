# Generated by Django 4.2.4 on 2024-09-28 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_rename_status_task_is_done_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('N', 'null')], default='todo', max_length=10),
        ),
    ]
