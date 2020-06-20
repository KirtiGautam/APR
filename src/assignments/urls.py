from django.urls import path

from .views import (
    assignments,
    getAssignments,
    assignmentDetail,
    vid,
    getSubjects,
    newAssignment,
    getLessons,
    getTest,
    addresource,
    video_watched
)

app_name = 'assignment'

urlpatterns = [
    path('assignment-video-mark-watched', video_watched, name='mark_watched'),
    path('assignments', assignments, name='assignments'),
    path('get-assignments', getAssignments, name='get_assignments'),
    path('assignment/<int:id>', assignmentDetail, name='assignmentDetails'),
    path('assignment/video/<int:id>', vid, name='video'),
    path('get-lesson', getLessons, name='get_lessons'),
    path('get-subjects', getSubjects, name='get_subjects'),
    path('add-new-assignment', newAssignment, name='newAssignment'),
    path('assignment/test/<int:id>', getTest, name='Test'),
    path('add-assignment-resource', addresource, name='addresource'),
]
