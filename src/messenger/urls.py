from django.urls import path, re_path

from .views import (index)
app_name = 'messenger'

urlpatterns = [
    path('messenger', index, name='index'),
]
