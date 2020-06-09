from django.db import models
from lessons.models import Subject, Lesson


class homework(models.Model):
    Name = models.CharField(max_length=255)
    Instructions = models.CharField(max_length=1000, default=None, null=True)
    date = models.DateField(auto_now_add=True)
    Subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='homework')


class video(models.Model):
    Name = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='homeworks/videos/', default=None, null=True)
    platform_choices = (
        ('Y', 'YOUTUBE'),
        ('L', 'LOCAL'),
    )
    platform = models.CharField(choices=platform_choices, max_length=1)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='homework_videos')
    homework = models.ForeignKey(
        homework, on_delete=models.CASCADE, related_name='videos')


class pdf(models.Model):
    Name = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='homworks/pdfs/', default=None, null=True)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='homework_pdfs')
    homework = models.ForeignKey(
        homework, on_delete=models.CASCADE, related_name='pdfs')


class test(models.Model):
    Name = models.CharField(max_length=50)
    homework = models.ForeignKey(
        homework, on_delete=models.CASCADE, related_name='Test')
    Lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='homework_Test')
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
        question, on_delete=models.CASCADE,  related_name='Answer')
    choice = models.ForeignKey(
        choice, on_delete=models.CASCADE, related_name='correct_choice')
