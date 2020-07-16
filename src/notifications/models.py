from django.db import models
from accounts.models import User


class notifs(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    link = models.URLField()
    read = models.BooleanField(default=False)
    recieved_date = models.DateTimeField(auto_now_add=True)
