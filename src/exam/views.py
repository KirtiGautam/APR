from django.shortcuts import render, redirect
from django import http
from accounts.models import Class
from exam.models import exam_type


def index(request):
    if request.user.is_authenticated or (request.user.admin or request.user.is_staff):
        data = {
            'classes': Class.objects.all() if request.user.admin else Class.objects.filter(Subject__teacher=request.user)
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
