from django.urls import path, re_path

from .views import (index)

app_name = 'exam'

urlpatterns = [
    path('exams', index, name='exams'),
]
