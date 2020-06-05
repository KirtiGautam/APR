from django.urls import path

from .views import (
    homeworks,
    getHomeworks,
    homeworkDetail,
    vid
)

app_name = 'homework'

urlpatterns = [
    path('homework', homeworks, name='homework'),
    path('get-homeworks', getHomeworks, name='get_homeworks'),
    path('homework/<int:id>', homeworkDetail, name='homeworkDetails'),
    path('homework/video/<int:id>', vid, name='video'),
]
