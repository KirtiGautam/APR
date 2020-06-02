from django.shortcuts import render, redirect
from accounts.models import Class
from django import http
from django.template.loader import render_to_string
from django.db.models import Q
from .models import pdf, video, Subject, Lesson


def assignments(request):
    if request.user.is_authenticated:
        return render(request, 'assignments/assignment.html')
    else:
        return redirect('accounts:login')


def lessons(request):
    if request.user.is_authenticated:
        if request.user.admin:
            classes = Class.objects.all()
            data = {
                'classes': classes
            }
            return render(request, 'lesson/lesson.html', data)
        else:
            return redirect('accounts:dashboard')
    else:
        return redirect('accounts:login')


def getLessons(request):
    if request.user.is_authenticated:
        if request.user.admin:
            if request.POST['subject'] == '':
                subject = Subject.objects.filter(Class=request.POST['id'])
            else:
                subject = Subject.objects.filter(id=request.POST['subject'])
            if subject:
                data = {
                    'pdfs': pdf.objects.filter(lesson__Subject=subject[0]),
                    'videos': video.objects.filter(lesson__Subject=subject[0]),
                }
            else:
                data = {}
            client = {
                'body': render_to_string('lesson/lessons.html', data),
                'subjects': list(Subject.objects.filter(Class=request.POST['id']).values('id', 'Name'))
            }
            return http.JsonResponse(client, safe=False)
        else:
            return http.HttpResponseForbidden
    else:
        return http.HttpResponseBadRequest
