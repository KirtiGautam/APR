# Generated by Django 3.0.3 on 2020-09-09 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('exam', '0005_auto_20200909_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Marks', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('File', models.FileField(blank=True, default=None, null=True, upload_to='StudentPaper/')),
                ('Paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StudentPaper', to='exam.Paper')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StudentPaper', to='accounts.Student')),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='Student',
            field=models.ManyToManyField(through='exam.StudentPaper', to='accounts.Student'),
        ),
    ]