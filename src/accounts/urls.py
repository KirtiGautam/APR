from django.urls import path
from .views import log, index, logo

app_name = 'accounts'

urlpatterns = [
    path('', index, name='dashboard'),
    path('login', log, name='login'),
    path('logout', logo, name='logout'),
]
