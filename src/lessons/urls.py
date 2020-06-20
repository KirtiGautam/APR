from django.urls import path
from lessons.views import (
    lessons,
    getLessons,
    getQuestions,
    addResource,
    video_watched,
    vid,
    getTest,
    pdf_read
)

app_name = 'lessons'

urlpatterns = [
    path('lessons', lessons, name='lessons'),
    path('get-lessons', getLessons, name='get_lessons'),
    path('get-questions', getQuestions, name='get-questions'),
    path('add-lesson-resource', addResource, name='add-lesson-resource'),
    path('video-mark-watched', video_watched, name='mark_watched'),
    path('lesson/video/<int:id>', vid, name='video'),
    path('lesson/test/<int:id>', getTest, name='Test'),
    path('mark-lesson-pdf-read', pdf_read, name='mark_read')
]
