from django.urls import path
from lessons.views import (
    lessons,
    getLessons,
    getQuestions,
    addResource,
    # upload,
    vid,
    getTest,
)

app_name = 'lessons'

urlpatterns = [
    path('lessons', lessons, name='lessons'),
    path('get-lessons', getLessons, name='get_lessons'),
    path('get-questions', getQuestions, name='get-questions'),
    path('add-lesson-resource', addResource, name='add-lesson-resource'),
    # path('upload', upload, name='upload'),
    path('lesson/video/<int:id>', vid, name='video'),
    path('lesson/test/<int:id>', getTest, name='Test')
]
