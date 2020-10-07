from django.urls import path
from .views import (index, mailed, reset)

app_name = 'security'

urlpatterns = [
    path('reset-password', index, name='index'),
    path('reset-password-mailed', mailed, name='mailed'),
    path('reset-password/<uuid:token>', reset, name='reset-password'),
]
