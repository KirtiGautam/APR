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
    Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_Test')
    final = models.BooleanField(default=False)


class Test_question(models.Model):
    question = models.ForeignKey(
        question, on_delete=models.CASCADE, related_name='lesson_test_questions')
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='question')
