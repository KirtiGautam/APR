from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('lessons.urls')),
    path('', include('assignments.urls')),
    path('', include('homework.urls')),
    path('', include('notifications.urls')),
    path('', include('exam.urls')),
    path('', include('messenger.urls')),
    path('', include('posts.urls')),
    path('', include('security.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
