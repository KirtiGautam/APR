from django.db import models
from accounts.models import User


class Message(models.Model):
    Sender = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='Messages')
    Body = models.TextField(blank=True, default=None, null=True)
    Asset = models.FileField(upload_to='message/',
                             blank=True, default=None, null=True)
    Created = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    Name = models.CharField(max_length=100)


class MessageRecipient(models.Model):
    Message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='Recipient')
    Recipient = models.ForeignKey(
        User, related_name='Recipient', on_delete=models.CASCADE)
    Group = models.ForeignKey(Group, related_name='recievers',
                              on_delete=models.CASCADE, blank=True, default=None, null=True)
    Read = models.BooleanField(default=False)


class UserGroup(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='Group')
    Group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='Users')
