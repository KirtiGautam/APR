from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django import http
from accounts.models import Class, User
from lessons.models import liveStream


def index(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'Class': Class.objects.all()
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
        client = {
            'livestream': liveStream.objects.filter(Class=Class.objects.get(id=request.GET['class']))
        }
        data = {
            'body': render_to_string('livestream/livestreams.html', context=client, request=request)
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def newLS(request):
    if request.user.is_authenticated:
        clas = Class.objects.get(id=request.POST['class'])
        teacher = User.objects.get(id=request.POST['teacher'])
        liveStream.objects.create(
            Class=clas, User=teacher, Name=request.POST['Name'], Stream_link=request.POST['Stream_link'], Time=request.POST['Time'], Duration=request.POST['Duration'])
        print([clas.name, teacher.get_full_name(), request.POST])
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
        livestream.save()
        data = {
            'message': 'Selected streams updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})
