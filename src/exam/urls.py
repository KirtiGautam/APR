from django.urls import path, re_path

from .views import (index, examSettings, deleteExam, updateExam, papers, delete, editPaper, deleteQuestion, editQuestion, markQuestion, addSection, editSection, finishPaper, instruction,
                    studentPaper, clearQuestion, finishExam, offlineGrade, publishResult, onlineGrade, GradeFile, Grade, publishExam, Results, proctored, importQuestions, faultCounter, paperDelete, paperDetails, confirmfinish)

from exam.report_gen import (test)

app_name = 'exam'

urlpatterns = [
    path('exams', index, name='exams'),
    path('paper/<int:id>', studentPaper, name='paper'),
    path('finish-paper-confirm/<int:id>',
         confirmfinish, name='confirm-paper-finish'),
    path('result/<int:id>', Results, name='results'),
    path('import-db-to-paper', importQuestions, name='db_import'),
    path('result-offline/<int:id>', offlineGrade, name='result-offline'),
    path('result-online/<int:id>', onlineGrade, name='result-online'),
    path('grade-file-online/<int:id>', GradeFile, name='grade-online'),
    path('grade-online/<int:id>', Grade, name='Grade-online'),
    path('paper-finished', finishExam, name='finished'),
    path('publish-result', publishResult, name='publish-result'),
    path('publish-result-exam', publishExam, name='publish-result-exam'),
    path('mark-paper-proctored', proctored, name='mark-proctored'),
    path('clear-student-choice/<int:id>', clearQuestion, name='clear-question'),
    path('exams/<int:id>', papers, name='papers'),
    path('paper-details', paperDetails, name='paper-details'),
    path('delete-paper', paperDelete, name='paper-delete'),
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
    path('exam-faults', faultCounter, name='exam-faults'),

    # Report Card
    path('generate-report-card/<int:id>', test, name='exam-report-card'),
]
