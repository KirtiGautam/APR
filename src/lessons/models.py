from django.db import models
from accounts.models import Class


class Subject(models.Model):
    Class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='Subject')
    Name = models.CharField(max_length=100)


class Lesson(models.Model):
    Name = models.CharField(max_length=255)
    Subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='Lesson')


class video(models.Model):
    Name = models.CharField(max_length=255)
    file = models.FileField(upload_to='lessons/videos/',
                            default=None, null=True)
    platform_choices = (
        ('Y', 'YOUTUBE'),
        ('L', 'LOCAL'),
    )
    platform = models.CharField(choices=platform_choices, max_length=1)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='lesson_videos')


class pdf(models.Model):
    Name = models.CharField(max_length=255)
    file = models.FileField(upload_to='lessons/pdfs/', default=None, null=True)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='lesson_pdfs')


class test(models.Model):
    Name = models.CharField(max_length=50)
    Lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='lesson_Test')
    final = models.BooleanField(default=False)


class question(models.Model):
    Name = models.CharField(max_length=500)
    test = models.ForeignKey(
        test, on_delete=models.CASCADE, related_name='question')


class choice(models.Model):
    Name = models.CharField(max_length=255)
    question = models.ForeignKey(
        question, on_delete=models.CASCADE, related_name='choice')


class answer(models.Model):
    question = models.OneToOneField(
        question, on_delete=models.CASCADE, related_name='Answer')
    choice = models.ForeignKey(
        choice, on_delete=models.CASCADE, related_name='correct_choice')
