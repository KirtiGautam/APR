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
    viewed_by = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)

    def is_viewed(self, user):
        return True if self.viewed_by.filter(id=user.id).exists() else False


class Pdf(models.Model):
    pdf = models.ForeignKey(pdf, on_delete=models.CASCADE,
                            related_name='lesson_pdfs')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='lesson_pdfs')
    viewed_by = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)

    def is_viewed(self, user):
        return True if self.viewed_by.filter(id=user.id).exists() else False


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
    created = models.DateTimeField(auto_now_add=True)


class user_progress_video(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watched_lesson_video')
    Video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='user_video')
    created = models.DateTimeField(auto_now_add=True)


class liveStream(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='livestream_duty')
    Subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='livestream')
    Name = models.CharField(max_length=100)
    Stream_link = models.URLField(max_length=2000)
    Time = models.DateTimeField()
    Duration = models.DecimalField(max_digits=4, decimal_places=2)

    def getduration(self):
        dura_string = str(self.Duration)
        dura_string = dura_string.split('.')
        if int(dura_string[0]) != 0:
            dura_string[0] += ' hrs'
            if int(dura_string[1]) != 0:
                dura_string[1] += ' mins'
            dura_string = ' '.join(dura_string)
        else:
            dura_string = dura_string[1] + ' mins'
        return dura_string


class Comment(models.Model):
    Video = models.ForeignKey(
        Video, related_name='comments', on_delete=models.CASCADE)
    Author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='lesson_video_comments')
    body = models.TextField()
    likes = models.ManyToManyField(User, through='lesson_video_likes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def is_liked(self, user):
        return True if self.likes.filter(id=user.id).exists() else False

    def getappreciates(self):
        return self.likes.filter(lesson_video_likes__User__user_type='Staff').count()

    def getlikes(self):
        return (self.likes.all().count() - self.getappreciates())

    def __str__(self):
        return self.Author.get_full_name()

    def when(self):
        from django.utils import timezone
        import math
        now = timezone.now()

        diff = now - self.created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class lesson_video_likes(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='lesson_video_likes')
    Comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
