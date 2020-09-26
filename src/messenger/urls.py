from django.urls import path
from .views import (index, getUsers, startChat, newMessages, newText, convos)

app_name = 'messenger'

urlpatterns = [
    path('messenger', index, name='index'),
    path('get-messages', startChat, name='messages'),
    path('send-message', newText, name='send-message'),
    path('get-conversations', convos, name='convos'),
    path('get-new-messages', newMessages, name='new-message'),
    path('search-users', getUsers, name='search-users'),
]
