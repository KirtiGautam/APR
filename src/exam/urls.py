from django.urls import path, re_path

from .views import (index, examSettings, deleteExam,
                    updateExam, papers, delete, editPaper)

app_name = 'exam'

urlpatterns = [
    path('exams', index, name='exams'),
    path('exams/<int:id>', papers, name='papers'),
    path('paper/edit/<int:id>', editPaper, name='edit-paper'),
    path('exam-delete', delete, name='delete'),
    path('exam-type-delete', deleteExam, name='delete-exam-type'),
    path('exam-type-update', updateExam, name='update-exam-type'),
    path('settings/exam-settings', examSettings, name='exam-settings'),
]
