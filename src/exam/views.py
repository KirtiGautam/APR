from django.shortcuts import render, redirect
from django import http
from accounts.models import Class
from lessons.models import Subject
from exam.models import (exam_type, Exam, Paper)
from django.utils import dateparse
import datetime
import pytz


def index(request):
    if request.user.is_authenticated:
        if request.method == "POST" and request.user.admin:
            exam = Exam.objects.create(exam_type=exam_type.objects.get(
                id=request.POST['exam_type']), Name=request.POST['exam_name'].strip(), Mode=request.POST['mode'])
            lis = []
            for i in range(1, int(request.POST['hidden_sn_count'])+1):
                Scheduled_on = dateparse.parse_datetime(
                    request.POST['dNt'+str(i)]).astimezone(tz=pytz.timezone("Asia/Kolkata"))
                Paper(Subject=Subject.objects.get(id=request.POST['subject'+str(i)]), Exam=exam, Scheduled_on=Scheduled_on, Duration=request.POST['duration'+str(
                    i)], Max_Marks=request.POST['max-marks' + str(i)], Pass_Marks=request.POST['pass-marks'+str(i)], Location=request.POST['location'+str(i)])
            Paper.objects.bulk_create(lis)
            return redirect("exam:exams")
        if request.user.admin:
            data = {
                'classes': Class.objects.all(),
                'Exams': Exam.objects.all(),
                'types': exam_type.objects.all()
            }
        elif request.user.is_staff:
            data = {
                'Exams': Exam.objects.filter(Paper__Subject__teacher=request.user),
                'classes': Class.objects.filter(Subject__teacher=request.user),
                'types': exam_type.objects.all()
            }
        return render(request, 'Exam/exams.html', data)
    return redirect('accounts:login')


def examSettings(request):
    if request.user.is_authenticated and request.user.admin:
        data = {}
        if request.method == "POST":
            obj, created = exam_type.objects.get_or_create(
                Name=request.POST['exam_name'].strip())
            if created:
                return redirect('exam:exam-settings')
            data['error'] = "Exam Type already exists"
        data['exams'] = exam_type.objects.all()
        return render(request, 'settings/admin/exams/examsSettings.html', data)
    return redirect('accounts:login')


def deleteExam(request):
    if request.user.is_authenticated and request.user.admin:
        if request.method == "POST":
            exam_type.objects.filter(id=request.POST['id']).delete()
            return redirect("exam:exam-settings")
    return redirect('accounts:login')


def updateExam(request):
    if request.user.is_authenticated and request.user.admin:
        if request.method == "POST":
            exam_type.objects.filter(id=request.POST['id']).update(
                Name=request.POST['exam_name'])
            return redirect("exam:exam-settings")
    return redirect('accounts:login')


def papers(request, id):
    if request.user.is_authenticated:
        exam = Exam.objects.get(id=id)
        if request.user.user_type == "Student" and not exam.objects.filter(Paper__Subject__Class=request.user.Student.Class).exists():
            return http.HttpResponseNotAllowed("Prohibhited")
        if request.user.is_staff and not exam.objects.filter(Paper__Subject__teacher=request.user).exist():
            return http.HttpResponseNotAllowed("Prohibhited")
        data = {
            'exam': exam
        }
        return render(request, "Exam/papers.html", data)
