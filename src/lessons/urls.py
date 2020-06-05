from django.urls import path
from .views import (
    lessons,
    getLessons,
    uploPage,
    vid,
)

app_name = 'lessons'

urlpatterns = [
    path('lessons', lessons, name='lessons'),
    path('get-lessons', getLessons, name='get_lessons'),
    path('upload', uploPage, name='upload'),
    path('lesson/video/<int:id>', vid, name='video'),
]
