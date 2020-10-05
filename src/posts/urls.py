from django.urls import path
from .views import (index,)

app_name = 'posts'

urlpatterns = [
    path('post', index, name='index'),
]
