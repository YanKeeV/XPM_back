from django.urls import path
from tasks import views

#from .views import ()

app_name = 'tasks'
urlpatterns = [
    # List view (Read all)
    path('', views.view_tasks, name='task-list'),

    path('<int:pk>', views.view_task, name='single-task'),

    # Create view
    path('create/', views.add_task, name='task-create'),

    # Update view
    path('update/<int:pk>', views.update_task, name='task-update'),

    # Delete view
    path('delete/<int:pk>', views.delete_task, name='task-destroy'),

    path('category', views.view_categories, name='category-list'),

    path('category/create/', views.add_category, name='category-create'),

    path('category/update/<int:pk>', views.update_category, name='category-update'),
    
    path('category/delete/<int:pk>', views.delete_category, name='category-destroy'),
]