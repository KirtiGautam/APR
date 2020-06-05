from django.urls import path

from .views import (
    assignments,
    getAssignments,
    assignmentDetail,
    vid
)

app_name = 'assignment'

urlpatterns = [
    path('assignments', assignments, name='assignments'),
    path('get-assignments', getAssignments, name='get_assignments'),
    path('assignment/<int:id>', assignmentDetail, name='assignmentDetails'),
    path('assignment/video/<int:id>', vid, name='video'),
]
