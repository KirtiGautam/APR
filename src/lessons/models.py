from django.db import models
from accounts.models import Class


class Subject(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)


class Lesson(models.Model):
    Name = models.CharField(max_length=255)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class video(models.Model):
    Name = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/', default=None, null=True)
    platform_choices = (
        ('Y', 'YOUTUBE'),
        ('L', 'LOCAL'),
    )
    platform = models.CharField(choices=platform_choices, max_length=1)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class pdf(models.Model):
    Name = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/', default=None, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
