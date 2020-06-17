from django.db import models
from lessons.models import Subject, Lesson, question
from accounts.models import video, pdf


class homework(models.Model):
    Name = models.CharField(max_length=255)
    Instructions = models.CharField(max_length=1000, default=None, null=True)
    date = models.DateField(auto_now_add=True)
    Subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='homework')


class Video(models.Model):
    video = models.ForeignKey(
        video, on_delete=models.CASCADE, related_name='homework_videos')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='homework_videos')


class Pdf(models.Model):
    pdf = models.ForeignKey(pdf, on_delete=models.CASCADE,
                            related_name='homework_pdfs')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='homework_pdfs')


class Test(models.Model):
    Name = models.CharField(max_length=50)
    Duration = models.CharField(max_length=10)
    Homework = models.ForeignKey(
        homework, on_delete=models.CASCADE, related_name='homework_Test')
    final = models.BooleanField(default=False)


class Test_question(models.Model):
    question = models.ForeignKey(
        question, on_delete=models.CASCADE, related_name='homework_test_questions')
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='question')
