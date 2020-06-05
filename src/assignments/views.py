from django.shortcuts import render, redirect
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import Class
from assignments.models import assignment, pdf, video
import datetime


def assignments(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name', 'section', 'year')
            }
            return render(request, 'assignments/assignment.html', data)
        else:
            return redirect('accounts:dashboard')

    else:
        return redirect('accounts:login')


def getAssignments(request):
    if request.user.is_authenticated:
        deads = []
        for x in assignment.objects.filter(
                Subject__Class=request.POST['id']):
            diff = x.Deadline-datetime.datetime.now(datetime.timezone.utc)
            deads.append({
                'assi': x,
                'days': diff.days,
                'hours': 24-datetime.datetime.now().hour,
                'minutes': 60-datetime.datetime.now().minute,
            })
        data = {
            'assignments': deads
        }
        client = {
            'body':  render_to_string('assignments/assignments.html', data),
            'done': True
        }
        return http.JsonResponse(client)
    else:
        http.HttpResponseForbidden


def assignmentDetail(request, id):
    if request.user.is_authenticated:
        data = {
            'assign': assignment.objects.get(id=id),
            'prefix': settings.MEDIA_URL,
        }
        return render(request, 'assignments/assignmentDetailView.html', data)
    else:
        return redirect('accounts:login')


def vid(request, id):
    if request.user.is_authenticated:
        videos = video.objects.get(id=id)
        return render(request, 'video/video.html', {'video': videos})
    else:
        return redirect('accounts:login')
