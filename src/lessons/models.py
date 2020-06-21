from django.db import models
from accounts.models import Class, User, video, pdf


class Subject(models.Model):
    Class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='Subject')
    Name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='teacher', default=None, null=True)
    backup_teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='backup_teacher', default=None, null=True)


class Lesson(models.Model):
    Number = models.PositiveIntegerField()
    Name = models.CharField(max_length=255)
    Subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='Lesson')


class question(models.Model):
    Name = models.CharField(max_length=500)
    difficulty_choices = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
        ('D', 'Difficult'),
    )
    Difficulty = models.CharField(choices=difficulty_choices, max_length=2)
    Lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='question')


class choice(models.Model):
    Name = models.CharField(max_length=255)
    question = models.ForeignKey(
        question, on_delete=models.CASCADE, related_name='choice')


class answer(models.Model):
    question = models.OneToOneField(
        question, on_delete=models.CASCADE,  related_name='Answer')
    choice = models.ForeignKey(
        choice, on_delete=models.CASCADE, related_name='correct_choice')


class Video(models.Model):
    video = models.ForeignKey(
        video, on_delete=models.CASCADE, related_name='lesson_videos')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='lesson_videos')


class Pdf(models.Model):
    pdf = models.ForeignKey(pdf, on_delete=models.CASCADE,
                            related_name='lesson_pdfs')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='lesson_pdfs')


class Test(models.Model):
    Name = models.CharField(max_length=50)
    Duration = models.CharField(max_length=10)
    Lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='lesson_Test')
    final = models.BooleanField(default=False)


class Test_question(models.Model):
    question = models.ForeignKey(
        question, on_delete=models.CASCADE, related_name='lesson_test_questions')
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='question')


class user_progress_pdf(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='read_lesson_pdf')
    Pdf = models.ForeignKey(
        Pdf, on_delete=models.CASCADE, related_name='user_pdf')


class user_progress_video(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watched_lesson_video')
    Video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='user_video')


class liveStream(models.Model):
    Class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='live_stream')
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='livestream_duty')
    Name = models.CharField(max_length=100)
    Stream_link = models.URLField(max_length=200)
    Time = models.DateTimeField()
    Duration = models.DecimalField(max_digits=4, decimal_places=2)
