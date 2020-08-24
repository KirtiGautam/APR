from django.shortcuts import render, redirect
from django import http


def index(request):
    if request.user.is_authenticated:
        return render(request, 'Exam/exams.html')
    return redirect('accounts:login')


def examSettings(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        if request.method == "GET":
            return render(request, 'settings/admin/exams/examsSettings.html')
        else:
            pass
    return redirect('accounts:login')
