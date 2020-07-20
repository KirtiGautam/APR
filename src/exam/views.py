from django.shortcuts import render, redirect
from django import http

def index(request):
    if request.user.is_authenticated:
        return render(request, 'Exam/exams.html')
    return redirect('accounts:login')
