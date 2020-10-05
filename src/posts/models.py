from django.db import models
from accounts.models import User


class Post(models.Model):
    Body = models.TextField(blank=True, default=None, null=True)
    Picture = models.ImageField(
        upload_to='Posts/', blank=True, default=None, null=True)
    Owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Post')
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
