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


class Announcement(models.Model):
    Title = models.CharField(max_length=100)
    Message = models.TextField()
    Recipient = models.ForeignKey(
        User, related_name='announcement', on_delete=models.CASCADE)
    Created = models.DateTimeField(auto_now_add=True)

    def when(self):
        time = self.Created
        import datetime as dt
        from datetime import datetime
        now = datetime.now(dt.timezone.utc)
        if type(time) is int:
            diff = now - datetime.fromtimestamp(time)
        elif isinstance(time, datetime):
            diff = now - time
        elif not time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(int(second_diff)) + " seconds ago"
            if second_diff < 120:
                return "a minute ago"
            if second_diff < 3600:
                return str(int(second_diff / 60)) + " minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str(int(second_diff / 3600)) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(int(day_diff)) + " days ago"
        if day_diff < 31:
            return str(int(day_diff / 7)) + " weeks ago"
        if day_diff < 365:
            return str(int(day_diff / 30)) + " months ago"
        return str(int(day_diff / 365)) + " years ago"
