from django.urls import path
from .views import (index, getUsers, startChat, newMessages, newText, convos, makeAnnouncement, announcements, oldMessages)

app_name = 'messenger'

urlpatterns = [
    path('messenger', index, name='index'),
    path('get-messages', startChat, name='messages'),
    path('send-message', newText, name='send-message'),
    path('get-conversations', convos, name='convos'),
    path('get-new-messages', newMessages, name='new-message'),
    path('get-old-messages', oldMessages, name='old-message'),
    path('search-users', getUsers, name='search-users'),
    path('make-announcement', makeAnnouncement, name='announcement'),
    path('announcements', announcements, name='announcements'),
]
