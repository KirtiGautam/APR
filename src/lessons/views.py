from django.shortcuts import render, redirect
from accounts.models import Class
from django import http
from django.template.loader import render_to_string
from django.db.models import Q
from .models import pdf, video, Subject, Lesson
from accounts.models import Student
from django.core.files.storage import default_storage
from django.conf import settings
import datetime


def assignments(request):
    if request.user.is_authenticated:
        if request.user.admin:
            classes = Class.objects.all()
            data = {
                'classes': classes
            }
            return render(request, 'assignments/assignment.html', data)
        else:
            return redirect('accounts:dashboard')

    else:
        return redirect('accounts:login')


def getAssignments(request):
    if request.user.is_authenticated:
        deads = []
        for x in Lesson.objects.filter(
                Subject__Class=request.POST['id'], assignment=True):
            diff = x.deadline-datetime.datetime.now(datetime.timezone.utc)
            deads.append({
                'assi': x,
                'days': diff.days,
                'hours': 24-datetime.datetime.now().hour,
                'minutes': 60-datetime.datetime.now().minute,
                'pdfs': pdf.objects.filter(lesson__id=x.id).count(),
                'videos': video.objects.filter(lesson__id=x.id).count(),
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
        LESS = Lesson.objects.get(id=id)
        data = {
            'pdfs': pdf.objects.filter(lesson=LESS),
            'videos': video.objects.filter(lesson=LESS),
            'prefix': settings.MEDIA_URL,
            'Title': LESS.Name,
            'Subject': LESS.Subject.Name,
        }
        return render(request, 'assignments/assignmentDetailView.html', data)
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
            data = {
                'class': Student.objects.get(user=request.user).Class.id
            }
            return render(request, 'lesson/lesson.html', data)
    else:
        return redirect('accounts:login')


def getLessons(request):
    if request.user.is_authenticated:
        if request.POST['subject'] == '':
            subject = Subject.objects.filter(Class=request.POST['id'])
        else:
            subject = Subject.objects.filter(id=request.POST['subject'])
        if subject:
            data = {
                'pdfs': pdf.objects.filter(lesson__Subject=subject[0], lesson__assignment=False),
                'videos': video.objects.filter(lesson__Subject=subject[0], lesson__assignment=False),
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
            pd = pdf.objects.create(
                Name=File, lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save('pdfs/'+str(pd.id)+'.pdf', file)
            pd.file = file_name
            pd.save()
        print([file, File])
        # file_name = default_storage.save(file.name, file)
        data = {
            'message': 'File uploaded!'
        }
        return http.JsonResponse(data)
