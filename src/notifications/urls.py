from django.urls import path, re_path
from notifications.views import (notifications)

app_name = 'notification'

urlpatterns = [
    path('get-all-notifications', notifications, name='notifs'),
]
