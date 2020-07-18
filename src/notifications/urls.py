from django.urls import path, re_path
from notifications.views import (notifications, read)

app_name = 'notification'

urlpatterns = [
    path('get-all-notifications', notifications, name='notifs'),
    path('notification-read', read, name='notifs-read'),
]
