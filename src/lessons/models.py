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

    def getlikes(self):
        all = self.likes.all().count()
        appreciates = self.likes.filter(
            lesson_video_likes__User__user_type='Staff').count()
        return "{} Appreciates {} Likes".format(appreciates, all-appreciates)

    def __str__(self):
        return self.Author.get_full_name()


class lesson_video_likes(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='lesson_video_likes')
    Comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
