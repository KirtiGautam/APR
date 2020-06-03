from django.urls import path
from .views import lessons, getLessons, assignments, uploPage, vid

app_name = 'lessons'

urlpatterns = [
    path('lessons', lessons, name='lessons'),
    path('get-lessons', getLessons, name='get_lessons'),
    path('assignments', assignments, name='assignments'),
    path('upload', uploPage, name='upload'),
    path('video/<int:id>', vid, name='video'),
]
