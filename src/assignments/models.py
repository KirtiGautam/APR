from django.db import models
from accounts.models import video, pdf, User
from lessons.models import Subject, Lesson, question


class assignment(models.Model):
    Name = models.CharField(max_length=255)
    Instructions = models.CharField(max_length=1000, default=None, null=True)
    Deadline = models.DateTimeField(default=None, null=True)
    Posted = models.DateTimeField(auto_now_add=True)
    Subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='assignments')


class Video(models.Model):
    video = models.ForeignKey(
        video, on_delete=models.CASCADE, related_name='assignment_videos')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='assignment_videos')
    assignment = models.ForeignKey(
        assignment, on_delete=models.CASCADE, related_name='video')


class Pdf(models.Model):
    pdf = models.ForeignKey(pdf, on_delete=models.CASCADE,
                            related_name='assignment_pdfs')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='assignment_pdfs')
    assignment = models.ForeignKey(
        assignment, on_delete=models.CASCADE, related_name='pdf')


class Test(models.Model):
    Name = models.CharField(max_length=50)
    Duration = models.CharField(max_length=10)
    Assignment = models.ForeignKey(
        assignment, on_delete=models.CASCADE, related_name='Test')
    final = models.BooleanField(default=False)


class Test_question(models.Model):
    question = models.ForeignKey(
        question, on_delete=models.CASCADE, related_name='assignment_test_questions')
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='question')


class user_progress_pdf(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='read_assignment_pdf')
    Pdf = models.ForeignKey(
        Pdf, on_delete=models.CASCADE, related_name='user_pdf')


class user_progress_video(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watched_assignment_video')
    Video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='user_video')


class AComment(models.Model):
    Video = models.ForeignKey(
        Video, related_name='comments', on_delete=models.CASCADE)
    Author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assignment_video_comments')
    body = models.TextField()
    likes = models.ManyToManyField(User, through='assignment_video_likes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def is_liked(self, user):
        return True if self.likes.filter(id=user.id).exists() else False

    def __str__(self):
        return self.Author.get_full_name()


class assignment_video_likes(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assignment_video_likes')
    AComment = models.ForeignKey(AComment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
