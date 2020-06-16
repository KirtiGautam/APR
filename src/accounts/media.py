from django.shortcuts import render, redirect
from accounts.models import pdf, video, Class, question, choice, answer
from lessons.models import Subject, Lesson
from django import http
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import json


def uploadQuestions(request):
    if request.user.is_authenticated and request.user.admin:
        lesson = Lesson.objects.get(id=request.POST['lesson'])
        for x in json.loads(request.POST['file']):
            qn = question.objects.create(
                Name=x['Question'], Lesson=lesson, Difficulty=x['Difficulty'])
            c1 = choice.objects.create(
                Name=x['Choice 1'].strip(), question=qn)
            c2 = choice.objects.create(
                Name=x['Choice 2'].strip(), question=qn)
            c3 = choice.objects.create(
                Name=x['Choice 3'].strip(), question=qn)
            c4 = choice.objects.create(
                Name=x['Choice 4'].strip(), question=qn)
            c = [c1, c2, c3, c4]
            for i in range(1, 5):
                if x['Choice '+str(i)].strip().lower() == x['Correct Answer'].strip().lower():
                    ans = answer.objects.create(question=qn, choice=c[i-1])
        data = {
            'message': 'File uploaded'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def questions(request):
    if request.user.is_authenticated and request.user.admin:
        data = {
            'class': Class.objects.all(),
            'question': question.objects.filter(Lesson__id=request.GET['lesson']),
        }
        return render(request, 'settings/admin/Allquestions/allquestions.html', data)
    return redirect('accounts:dashboard')


def allquestions(request):
    if request.user.is_authenticated and request.user.admin:
        data = {
            'class': Class.objects.all()
        }
        return render(request, 'settings/admin/Allquestions/allquestions.html', data)
    return redirect('accounts:dashboard')


def allmedia(request):
    if request.user.is_authenticated and request.user.admin:
        return render(request, 'settings/admin/AllMedia/allmedia.html')
    return redirect('accounts:dashboard')


def upload(request):
    if request.user.is_authenticated and request.user.admin:
        if request.POST['dataType'] == 'pdf':
            file = request.FILES['file']
            fs = FileSystemStorage()
            name = fs.save('pdfs/'+file.name, file)
            pdf.objects.create(
                Name=request.POST['Name'], Description=request.POST['description'], file=name)
            data = {
                'url': fs.url(name)
            }
        elif request.POST['dataType'] == 'video':
            if request.POST['videoType'] == 'local':
                file = request.FILES['file']
                fs = FileSystemStorage()
                name = fs.save('videos/'+file.name, file)
                video.objects.create(
                    Name=request.POST['Name'], Description=request.POST['description'], file=name)
                data = {
                    'url': fs.url(name)
                }
            if request.POST['videoType'] == 'youtube':
                file = request.POST['file']
                video.objects.create(
                    Name=request.POST['Name'], Description=request.POST['description'], file=file, Local=False)
                data = {
                    'url': file
                }
        else:
            data = {
                'message': 'Undefined Media type uploaded'
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def getMedia(request):
    if request.user.is_authenticated and request.user.admin:
        if request.POST['type'] == 'video':
            data = {
                'video': list(video.objects.all().values('Name', 'Description', 'Local', 'file'))
            }
        elif request.POST['type'] == 'pdf':
            data = {
                'pdf': list(pdf.objects.all().values('Name', 'Description', 'file'))
            }
        else:
            data = {
                'video': list(video.objects.all().values('Name', 'Description', 'Local', 'file')),
                'pdf': list(pdf.objects.all().values('Name', 'Description', 'file'))
            }
        data['prefix'] = settings.MEDIA_URL
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})
