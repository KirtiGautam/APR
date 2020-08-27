from django.urls import path, re_path

from .views import (index, examSettings, deleteExam, updateExam, papers)

app_name = 'exam'

urlpatterns = [
    path('exams', index, name='exams'),
    path('exams/<int:id>', papers, name='papers'),
    path('exam-type-delete', deleteExam, name='delete-exam-type'),
    path('exam-type-update', updateExam, name='update-exam-type'),
    path('settings/exam-settings', examSettings, name='exam-settings'),
]
