from django.urls import path, re_path

from .views import (
    homeworks,
    getHomeworks,
    homeworkDetail,
    vid,
    getTest,
    addresource,
    newHomework,
    video_watched,
    pdf_read,
    deleteMedia,
    HomeDetails,
    updateDetails,
    studentStats
)

app_name = 'homework'

urlpatterns = [
    path('homework-video-mark-watched', video_watched, name='mark_watched'),
    path('homework', homeworks, name='homework'),
    path('get-homeworks', getHomeworks, name='get_homeworks'),
    path('homework/<int:id>', homeworkDetail, name='homeworkDetails'),
    path('homework/video/<int:id>', vid, name='video'),
    path('add-new-homework', newHomework, name='newHomework'),
    path('homework/test/<int:id>', getTest, name='Test'),
    path('add-homework-resource', addresource, name='addresource'),
    path('mark-homework-pdf-read', pdf_read, name='pdf-read'),
    path('delete-homework-media', deleteMedia, name='media-delete'),
    path('get-homework-details', HomeDetails, name='homework-details'),
    path('update-homework-details', updateDetails,
         name='update-homework-details'),
    re_path(r'^homework-student-stats$', studentStats, name='student-stats'),
]
