from django.shortcuts import render, redirect
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import Class
from homework.models import homework, pdf, video
import datetime


def homeworks(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name', 'section', 'year')
            }
            return render(request, 'homeworks/homework.html', data)
        else:
            return redirect('accounts:dashboard')
    else:
        return redirect('accounts:login')


def getHomeworks(request):
    if request.user.is_authenticated:
        data = {
            'homeworks': homework.objects.filter(
                Subject__Class=request.POST['id'], date=request.POST['date'])
        }
        client = {
            'body':  render_to_string('homeworks/homeworks.html', data),
            'done': True
        }
        return http.JsonResponse(client)
    else:
        http.HttpResponseForbidden


def homeworkDetail(request, id):
    if request.user.is_authenticated:
        data = {
            'homework': homework.objects.get(id=id),
            'prefix': settings.MEDIA_URL,
        }
        return render(request, 'homeworks/homeworkDetailView.html', data)
    else:
        return redirect('accounts:login')


def vid(request, id):
    if request.user.is_authenticated:
        videos = video.objects.get(id=id)
        return render(request, 'video/video.html', {'video': videos})
    else:
        return redirect('accounts:login')
