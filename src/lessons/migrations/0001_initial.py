# Generated by Django 3.0.3 on 2020-09-16 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('doubt', models.BooleanField(default=False)),
                ('resolved', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_video_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.PositiveIntegerField()),
                ('Name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Pdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_pdfs', to='lessons.Lesson')),
                ('pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_pdfs', to='accounts.pdf')),
                ('viewed_by', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=500)),
                ('Difficulty', models.CharField(choices=[('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'), ('D', 'Difficult')], max_length=2)),
                ('Lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='lessons.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Duration', models.CharField(max_length=10)),
                ('final', models.BooleanField(default=False)),
                ('Lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_Test', to='lessons.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_videos', to='lessons.Lesson')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_videos', to='accounts.video')),
                ('viewed_by', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='user_progress_video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched_lesson_video', to=settings.AUTH_USER_MODEL)),
                ('Video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_video', to='lessons.Video')),
            ],
        ),
        migrations.CreateModel(
            name='user_progress_pdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pdf', to='lessons.Pdf')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_lesson_pdf', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test_question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_test_questions', to='lessons.question')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='lessons.Test')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Subject', to='accounts.Class')),
                ('backup_teacher', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backup_teacher', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='liveStream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Stream_link', models.URLField(max_length=2000)),
                ('Time', models.DateTimeField()),
                ('Duration', models.DecimalField(decimal_places=2, max_digits=4)),
                ('Subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livestream', to='lessons.Subject')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livestream_duty', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='lesson_video_likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('Comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.Comment')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_video_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='Subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Lesson', to='lessons.Subject'),
        ),
        migrations.AddField(
            model_name='comment',
            name='Video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='lessons.Video'),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(through='lessons.lesson_video_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='lessons.Comment'),
        ),
        migrations.CreateModel(
            name='choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice', to='lessons.question')),
            ],
        ),
        migrations.CreateModel(
            name='answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explanation', models.TextField()),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correct_choice', to='lessons.choice')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Answer', to='lessons.question')),
            ],
        ),
    ]
