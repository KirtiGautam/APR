from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django import http
from accounts.models import Class, User
from lessons.models import liveStream, Subject
from django.utils import timezone, dateparse


def index(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'Class': Class.objects.all()
            }
        elif request.user.is_staff:
            data = {
                'class': request.user.teacher.all()
            }
        else:
            data = {
                'Class': request.user.Student.Class.id
            }
        return render(request, 'livestream/livestream.html', data)
    else:
        return redirect('accounts:login')


def livestreams(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            ls = request.user.livestream_duty.filter(Subject__Class=Class.objects.get(
                id=request.GET['class']), Time__gt=timezone.now())
        else:
            ls = liveStream.objects.filter(Subject__Class=Class.objects.get(
                id=request.GET['class']), Time__gt=timezone.now())
        client = {
            'livestream': ls
        }
        data = {
            'body': render_to_string('livestream/livestreams.html', context=client, request=request)
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def newLS(request):
    if request.user.is_authenticated:
        time = timezone.make_aware(
            dateparse.parse_datetime(request.POST['Time']))
        subject = Subject.objects.get(id=request.POST['Subject'])
        teacher = User.objects.get(id=request.POST['teacher'])
        liveStream.objects.create(
            Subject=subject, User=teacher, Name=request.POST['Name'], Stream_link=request.POST['Stream_link'], Time=time, Duration=request.POST['Duration'])
        data = {
            'message': 'Live Stream added'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def deleteStream(request):
    if request.user.is_authenticated:
        liveStream.objects.filter(
            id__in=request.POST.getlist('data[]')).delete()
        data = {
            'message': 'Selected streams deleted'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def getStream(request):
    if request.user.is_authenticated:
        LS = liveStream.objects.get(id=request.GET['id'])

        data = {
            'teacher': LS.User.id,
            'Name': LS.Name,
            'Stream_link': LS.Stream_link,
            'Time': LS.Time,
            'Duration': LS.Duration,
            'Subject': LS.Subject.id
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def editStream(request):
    if request.user.is_authenticated:
        livestream = liveStream.objects.get(id=request.POST['id'])
        livestream.Name = request.POST['Name']
        livestream.Stream_link = request.POST['Stream_link']
        livestream.Duration = request.POST['Duration']
        livestream.Time = request.POST['Time']
        livestream.User = User.objects.get(id=request.POST['teacher'])
        livestream.Subject = Subject.objects.get(id=request.POST['Subject'])
        livestream.save()
        data = {
            'message': 'Selected streams updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})
