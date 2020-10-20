# Generated by Django 3.0.3 on 2020-10-07 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homework', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='homework_pdf_likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_pdf_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='pdfHComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('doubt', models.BooleanField(default=False)),
                ('resolved', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_pdf_comments', to=settings.AUTH_USER_MODEL)),
                ('Pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='homework.Pdf')),
                ('likes', models.ManyToManyField(through='homework.homework_pdf_likes', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='homework.pdfHComment')),
            ],
        ),
        migrations.AddField(
            model_name='homework_pdf_likes',
            name='pdfHComment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.pdfHComment'),
        ),
    ]