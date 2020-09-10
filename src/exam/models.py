from django.db import models
from lessons.models import Subject
from accounts.models import Student
import datetime
import pytz


class exam_type(models.Model):
    Name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Exam(models.Model):
    mode_choices = (
        ('C', 'Classroom'),
        ('O', 'Online'),
    )
    Name = models.CharField(max_length=255)
    Mode = models.CharField(max_length=2, choices=mode_choices)
    exam_type = models.ForeignKey(
        exam_type, on_delete=models.CASCADE, related_name='Exams')

    def range(self):
        all = self.Paper.all().order_by('Scheduled_on')
        first = all.first().Scheduled_on
        last = all.last().Scheduled_on
        return {'first': first, 'last': last}

    def expired(self):
        last = self.Paper.all().order_by('Scheduled_on').last()
        last.Scheduled_on += datetime.timedelta(minutes=last.Duration)
        expire = True if last.Scheduled_on < datetime.datetime.now(
            pytz.utc) else False
        return expire


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
    Result = models.BooleanField(default=False)
    Student = models.ManyToManyField(Student, through='StudentPaper')

    def pattern(self):
        return 'Objective' if self.Exam.Mode == 'O' and self.Question.all().count() == self.Question.filter(Type='O').count() else 'Multiple'

    def left(self):
        if self.Exam.Mode == 'C' or self.File:
            lef = StudentPaper.objects.filter(Paper=self, Marks__isnull=True).exists(
            ) and StudentPaper.objects.filter(Paper=self, Marks__isnull=False).exists()
        else:
            lef = StudentAttempt.objects.filter(Question__Paper=self, Marks__isnull=True).exists(
            ) and StudentAttempt.objects.filter(Question__Paper=self, Marks__isnull=False).exists()
        return lef


class StudentPaper(models.Model):
    Paper = models.ForeignKey(
        Paper, related_name='StudentPaper', on_delete=models.CASCADE)
    Student = models.ForeignKey(
        Student, related_name='StudentPaper', on_delete=models.CASCADE)
    Marks = models.PositiveIntegerField(null=True, blank=True, default=None)
    Done = models.BooleanField(default=False)
    File = models.FileField(upload_to='StudentPaper/',
                            null=True, blank=True, default=None)


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
    Student = models.ManyToManyField(Student, through='StudentAttempt')

    def attempted(self, user):
        return self.Student.filter(user=user).exists()

    def which(self, user):
        return StudentAttempt.objects.get(Student=user.Student, Question=self).Option

    def what(self, user):
        return StudentAttempt.objects.get(Student=user.Student, Question=self).Text

    def number(self, user):
        lis = StudentAttempt.objects.get(
            Student=user.Student, Question=self).Text.split("','")
        return lis


class Option(models.Model):
    Question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="Option")
    Text = models.TextField(null=True, blank=True, default=None)
    Asset = models.ImageField(
        upload_to="Option_asset/", null=True, blank=True, default=None)


class StudentAttempt(models.Model):
    Question = models.ForeignKey(
        Question, related_name='Exam_attempts', on_delete=models.CASCADE)
    Student = models.ForeignKey(
        Student, related_name='Exam_attempts', on_delete=models.CASCADE)
    Option = models.ForeignKey(Option, related_name='Student_attempt',
                               on_delete=models.CASCADE, null=True, blank=True, default=None)
    Text = models.TextField(null=True, blank=True, default=None)
    Marks = models.PositiveIntegerField(null=True, blank=True, default=None)


class Answer(models.Model):
    Question = models.OneToOneField(
        Question, related_name="Answer", on_delete=models.CASCADE)
    Explanation = models.TextField()
    Option = models.ForeignKey(
        Option, related_name="Answer", on_delete=models.CASCADE, null=True, blank=True, default=None)

    def get_blanks(self):
        lis = self.Explanation.split("','")
        return lis
