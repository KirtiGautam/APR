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
    File = models.BooleanField(default=False)
    Scheduled_on = models.DateTimeField()
    Duration = models.PositiveIntegerField()
    Max_Marks = models.PositiveIntegerField()
    Pass_Marks = models.PositiveIntegerField()
    Location = models.CharField(max_length=100)


class Section(models.Model):
    Paper = models.ForeignKey(
        Paper, related_name='Section', on_delete=models.CASCADE)
    Start = models.PositiveIntegerField()
    End = models.PositiveIntegerField()


class Question(models.Model):
    paper_type_choices = (
        ('O', 'Objective'),
        ('S', 'Short Answer'),
        ('L', 'Long Answer'),
        ('U', 'Fill Ups'),
    )
    SNo = models.PositiveIntegerField()
    Text = models.TextField(null=True, blank=True, default=None)
    Asset = models.ImageField(
        upload_to='Question_asset/', null=True, blank=True, default=None)
    Paper = models.ForeignKey(
        Paper, related_name="Question", on_delete=models.CASCADE)
    Type = models.CharField(max_length=2, choices=paper_type_choices)
    Max_Marks = models.PositiveIntegerField()


class Option(models.Model):
    Question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="Option")
    Text = models.TextField(null=True, blank=True, default=None)
    Asset = models.ImageField(
        upload_to="Option_asset/", null=True, blank=True, default=None)


class Answer(models.Model):
    Question = models.OneToOneField(
        Question, related_name="Answer", on_delete=models.CASCADE)
    Explanation = models.TextField()
    Option = models.ForeignKey(
        Option, related_name="Answer", on_delete=models.CASCADE, null=True, blank=True, default=None)

    def get_blanks(self):
        lis = self.Explanation.split("','")
        return lis
