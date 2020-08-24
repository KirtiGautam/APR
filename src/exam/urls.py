from django.urls import path, re_path

from .views import (index, examSettings)

app_name = 'exam'

urlpatterns = [
    path('exams', index, name='exams'),
    path('settings/exam-settings', examSettings, name='exam-setiings'),
]
