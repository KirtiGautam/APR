from django.urls import path
from .views import lessons, getLessons, assignments

app_name = 'lessons'

urlpatterns = [
    path('lessons', lessons, name='lessons'),
    path('get-lessons', getLessons, name='get_lessons'),
    path('assignments', assignments, name='assignments'),
]
