# Generated by Django 3.0.3 on 2020-07-04 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default='2020-07-05'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default='2020-07-05'),
            preserve_default=False,
        ),
    ]
