from django.urls import path
from notes import views

app_name = 'notes'
urlpatterns = [
    # List view (Read all)
    path('', views.view_notes, name='note-list'),

    path('<int:pk>', views.view_note, name='single-note'),

    # Create view
    path('create/', views.add_note, name='note-create'),

    # Update view
    path('update/<int:pk>', views.update_note, name='note-update'),

    # Delete view
    path('delete/<int:pk>', views.delete_note, name='note-destroy'),

    path('tags', views.view_tags, name='tag-list'),

    path('tag/create/', views.add_tag, name='tag-create'),

    path('tag/update/<int:pk>', views.update_tag, name='tag-update'),
    
    path('tag/delete/<int:pk>', views.delete_tag, name='tag-destroy'),
]