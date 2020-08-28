from django.db import models
from lessons.models import Subject


class exam_type(models.Model):
    Name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Exam(models.Model):
    mode_choices = (
        ('C', 'Classroom'),
        ('O', 'Offline'),
    )
    Name = models.CharField(max_length=255)
    Mode = models.CharField(max_length=2, choices=mode_choices)
    exam_type = models.ForeignKey(
        exam_type, on_delete=models.CASCADE, related_name='Exams')


class Paper(models.Model):
    Subject = models.ForeignKey(
        Subject, related_name="Paper", on_delete=models.CASCADE)
    Exam = models.ForeignKey(
        Exam, related_name="Paper", on_delete=models.CASCADE)
    Published = models.BooleanField(default=False)
    Scheduled_on = models.DateTimeField()
    Duration = models.PositiveIntegerField()
    Max_Marks = models.PositiveIntegerField()
    Pass_Marks = models.PositiveIntegerField()
    Location = models.CharField(max_length=100)


class Question(models.Model):
    paper_type_choices = (
        ('O', 'Objective'),
        ('S', 'Short Answer'),
        ('L', 'Long Answer'),
        ('U', 'Fill Ups'),
        ('F', 'File Submission'),
    )
    SNo = models.PositiveIntegerField()
    Text = models.TextField()
    Asset = models.ImageField(upload_to='Question_asset/')
    Paper = models.ForeignKey(
        Paper, related_name="Question", on_delete=models.CASCADE)
    Type = models.CharField(max_length=2, choices=paper_type_choices)
    Max_Marks = models.PositiveIntegerField()
