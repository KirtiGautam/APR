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
