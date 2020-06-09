from django.urls import path

from .views import (
    assignments,
    getAssignments,
    assignmentDetail,
    vid,
    getSubjects,
    newAssignment,
    getLessons,
    Test
)

app_name = 'assignment'

urlpatterns = [
    path('assignments', assignments, name='assignments'),
    path('get-assignments', getAssignments, name='get_assignments'),
    path('assignment/<int:id>', assignmentDetail, name='assignmentDetails'),
    path('assignment/video/<int:id>', vid, name='video'),
    path('get-lesson', getLessons, name='get_lessons'),
    path('get-subjects', getSubjects, name='get_subjects'),
    path('newAssignment', newAssignment, name='newAssignment'),
    path('assignment/test/<int:id>', Test, name='Test'),
]
