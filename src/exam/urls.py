from django.urls import path, re_path

from .views import (index, examSettings, deleteExam, updateExam, papers, delete, editPaper, deleteQuestion, editQuestion, markQuestion, addSection, editSection, finishPaper, instruction, studentPaper, clearQuestion, finishExam, offlineGrade, publishResult, onlineGrade, GradeFile)

app_name = 'exam'

urlpatterns = [
    path('exams', index, name='exams'),
    path('paper/<int:id>', studentPaper, name='paper'),
    path('result-offline/<int:id>', offlineGrade, name='result-offline'),
    path('result-online/<int:id>', onlineGrade, name='result-online'),
    path('grade-file-online/<int:id>', GradeFile, name='grade-online'),
    path('paper-finished', finishExam, name='finished'),
    path('publish-result', publishResult, name='publish-result'),
    path('clear-student-choice/<int:id>', clearQuestion, name='clear-question'),
    path('exams/<int:id>', papers, name='papers'),
    path('paper/edit/<int:id>', editPaper, name='edit-paper'),
    path('paper/instructions/<int:id>', instruction, name='paper-instruction'),
    path('finish-paper-edit/<int:id>', finishPaper, name='finish-paper-edit'),
    path('question/delete/<int:id>', deleteQuestion, name='delete-question'),
    path('add-section', addSection, name='add-section'),
    path('edit-section/<int:id>', editSection, name='edit-section'),
    path('edit-question-details', editQuestion, name='edit-question-details'),
    path('mark-question-file', markQuestion, name='mark-question-file'),
    path('exam-delete', delete, name='delete'),
    path('exam-type-delete', deleteExam, name='delete-exam-type'),
    path('exam-type-update', updateExam, name='update-exam-type'),
    path('settings/exam-settings', examSettings, name='exam-settings'),
]
