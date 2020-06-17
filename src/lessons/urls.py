from django.urls import path
from lessons.views import (
    lessons,
    getLessons,
    # upload,
    # vid,
    # Test,
)

app_name = 'lessons'

urlpatterns = [
    path('lessons', lessons, name='lessons'),
    path('get-lessons', getLessons, name='get_lessons'),
    # path('upload', upload, name='upload'),
    # path('lesson/video/<int:id>', vid, name='video'),
    # path('lesson/test/<int:id>', Test, name='Test')
]
