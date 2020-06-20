from django.db import models
from lessons.models import Subject, Lesson, question
from accounts.models import video, pdf, User


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
    homework = models.ForeignKey(
        homework, on_delete=models.CASCADE, related_name='video')


class Pdf(models.Model):
    pdf = models.ForeignKey(pdf, on_delete=models.CASCADE,
                            related_name='homework_pdfs')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='homework_pdfs')
    homework = models.ForeignKey(
        homework, on_delete=models.CASCADE, related_name='pdf')


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


class user_progress_pdf(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='read_homework_pdf')
    Pdf = models.ForeignKey(
        Pdf, on_delete=models.CASCADE, related_name='user_pdf')


class user_progress_video(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watched_homework_video')
    Video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='user_video')
