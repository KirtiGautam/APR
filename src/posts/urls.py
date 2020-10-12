from django.urls import path
from .views import (index, likePost, single,
                    likePostComment, updatePost, deletePost)

app_name = 'posts'

urlpatterns = [
    path('post', index, name='index'),
    path('like-post', likePost, name='like-Post'),
    path('like-post-comment', likePostComment, name='like-Post-comment'),
    path('post/<int:id>', single, name='post'),
    path('delete/post/<int:id>', deletePost, name='delete'),
    path('update/post', updatePost, name='update'),
]
