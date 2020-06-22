from django.urls import path, re_path
from accounts.user_settings import (
    changePassword
    )

urlpatterns = [
    path('settings/change-password', changePassword, name='change-password'),
]