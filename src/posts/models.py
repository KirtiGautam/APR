from django.db import models
from accounts.models import User


class Post(models.Model):
    Body = models.TextField(blank=True, default=None, null=True)
    Picture = models.ImageField(
        upload_to='Posts/', blank=True, default=None, null=True)
    Owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Post')
    Tag_choices = (
        ('D', 'Doubts'),
        ('A', 'Announcements'),
        ('L', 'Deadlines'),
    )
    Tag = models.CharField(max_length=2, choices=Tag_choices,
                           default=None, null=True, blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    Likes = models.ManyToManyField(User, through='Likes')

    def comments(self):
        return self.Comments.filter(parent__isnull=True)


class Likes(models.Model):
    User = models.ForeignKey(
        User, related_name='PostLike', on_delete=models.CASCADE)
    Post = models.ForeignKey(Post, related_name='Like',
                             on_delete=models.CASCADE)
    Created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    Post = models.ForeignKey(
        Post, related_name='Comments', on_delete=models.CASCADE)
    Author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Post_Comment')
    body = models.TextField()
    Likes = models.ManyToManyField(User, related_name='Likes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def is_liked(self, user):
        return True if self.likes.filter(id=user.id).exists() else False

    def when(self):
        from django.utils import timezone
        import math
        now = timezone.now()

        diff = now - self.created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"
