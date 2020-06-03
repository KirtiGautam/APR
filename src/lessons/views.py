from django.shortcuts import render, redirect
from accounts.models import Class
from django import http
from django.template.loader import render_to_string
from django.db.models import Q
from .models import pdf, video, Subject, Lesson
from django.core.files.storage import default_storage
from django.conf import settings


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
                    'prefix': settings.MEDIA_URL,
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


def vid(request, id):
    if request.user.is_authenticated:
        videos = video.objects.get(id=id)
        return render(request, 'video/video.html', {'video': videos})
    else:
        return redirect('accounts:login')


def uploPage(request):
    if request.method == 'GET':
        return render(request, 'video.html')
    else:
        file = request.FILES['file']
        File = request.POST['name']
        lessson = request.POST['lesson']
        if request.POST['type'] == 'video':
            vid = video.objects.create(
                Name=File, platform='L', lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save(
                'videos/'+str(vid.id)+'.mp4', file)
            vid.file = file_name
            vid.save()
        else:
            pdf = pdf.objects.create(
                Name=File, lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save('pdfs/'+str(vid.id)+'.pdf', file)
            pdf.file = file_name
            pdf.save()
        print([file, File])
        # file_name = default_storage.save(file.name, file)
        data = {
            'message': 'File uploaded!'
        }
        return http.JsonResponse(data)
