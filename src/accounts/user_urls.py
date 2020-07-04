from django.urls import path, re_path
from accounts.user_settings import (
    changePassword,
)
from accounts.leaderboard import leaderboard

urlpatterns = [
    path('settings/change-password', changePassword, name='change-password'),
    path('leaderboard', leaderboard, name='leaderboard'),
]
