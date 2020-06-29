# Generated by Django 3.0.3 on 2020-06-28 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lessons', '0001_initial'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Instructions', models.CharField(default=None, max_length=1000, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('Subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework', to='lessons.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Pdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdf', to='homework.homework')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_pdfs', to='lessons.Lesson')),
                ('pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_pdfs', to='accounts.pdf')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Duration', models.CharField(max_length=10)),
                ('final', models.BooleanField(default=False)),
                ('Homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_Test', to='homework.homework')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video', to='homework.homework')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_videos', to='lessons.Lesson')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_videos', to='accounts.video')),
            ],
        ),
        migrations.CreateModel(
            name='user_progress_video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched_homework_video', to=settings.AUTH_USER_MODEL)),
                ('Video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_video', to='homework.Video')),
            ],
        ),
        migrations.CreateModel(
            name='user_progress_pdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pdf', to='homework.Pdf')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_homework_pdf', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test_question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_test_questions', to='lessons.question')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='homework.Test')),
            ],
        ),
    ]
