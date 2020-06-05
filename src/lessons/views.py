from django.shortcuts import render, redirect
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
from accounts.models import Class, Student
from lessons.models import pdf, video, Subject, Lesson


def lessons(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name', 'section', 'year')
            }
            return render(request, 'lesson/lesson.html', data)
        else:
            data = {
                'class': request.user.Student.Class.id
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
                'lessons': subject[0].Lesson.all(),
                'prefix': settings.MEDIA_URL,
                'admin': request.user.admin,
            }
        else:
            data = {}
        client = {
            'body': render_to_string('lesson/lessons.html', data),
            'subjects': list(Subject.objects.filter(Class=request.POST['id']).values('id', 'Name'))
        }
        return http.JsonResponse(client, safe=False)
    else:
        return http.HttpResponseForbidden({'messsage': 'You are not authorized for this request'})


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
                'lessons/videos/'+str(vid.id)+'.mp4', file)
            vid.file = file_name
            vid.save()
        else:
            pd = pdf.objects.create(
                Name=File, lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save(
                'lessons/pdfs/'+str(pd.id)+'.pdf', file)
            pd.file = file_name
            pd.save()
        data = {
            'message': 'File uploaded!'
        }
        return http.JsonResponse(data)
