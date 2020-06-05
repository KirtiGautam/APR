from django.db import models
from lessons.models import Subject, Lesson


class assignment(models.Model):
    Name = models.CharField(max_length=255)
    Instructions = models.CharField(max_length=1000, default=None, null=True)
    Deadline = models.DateTimeField(default=None, null=True)
    Subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='assignments')


class video(models.Model):
    Name = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='assignments/videos/', default=None, null=True)
    platform_choices = (
        ('Y', 'YOUTUBE'),
        ('L', 'LOCAL'),
    )
    platform = models.CharField(choices=platform_choices, max_length=1)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='assignment_videos')
    assignment = models.ForeignKey(
        assignment, on_delete=models.CASCADE, related_name='videos')


class pdf(models.Model):
    Name = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='assignments/pdfs/', default=None, null=True)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='assignment_pdfs')
    assignment = models.ForeignKey(
        assignment, on_delete=models.CASCADE, related_name='pdfs')
