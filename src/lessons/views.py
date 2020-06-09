from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
from accounts.models import Class, Student
from lessons.models import pdf, video, Subject, Lesson, test, question, choice, answer
import json


def Test(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            data = {
                'test': test.objects.get(id=id),
                'url': reverse('lessons:Test', args=[id]),
            }
            return render(request, 'test/test.html', data)
        else:
            Test = test.objects.get(id=id).question.all()
            correct = 0
            for x in Test:
                if request.POST[str(x.id)] != '':
                    if int(request.POST[str(x.id)]) == x.Answer.choice.id:
                        correct += 1
            data = {
                'Number': Test.count(),
                'Percentage': (correct/Test.count())*100,
                'Correct': correct,
                'Wrong': Test.count()-correct,
            }
            return render(request, 'test/result.html', data)
    else:
        return redirect('accounts:login')


def lessons(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name', 'section', 'year')
            }
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


def upload(request):
    if request.method == 'GET':
        return redirect('accounts:dashboard')
    else:
        File = request.POST['name']
        if request.POST['type'] == 'video':
            file = request.FILES['file']
            vid = video.objects.create(
                Name=File, platform='L', lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save(
                'lessons/videos/'+str(vid.id)+'.mp4', file)
            vid.file = file_name
            vid.save()
        elif request.POST['type'] == 'csv':
            Tobj = test.objects.create(
                Name=File, Lesson=Lesson.objects.get(id=request.POST['lesson']))
            for x in json.loads(request.POST['file']):
                qn = question.objects.create(Name=x['Question'], test=Tobj)
                c1 = choice.objects.create(
                    Name=x['Choice 1'].trim(), question=qn)
                c2 = choice.objects.create(
                    Name=x['Choice 2'].trim(), question=qn)
                c3 = choice.objects.create(
                    Name=x['Choice 3'].trim(), question=qn)
                c4 = choice.objects.create(
                    Name=x['Choice 4'].trim(), question=qn)
                c = [c1, c2, c3, c4]
                for i in range(1, 5):
                    if x['Choice '+str(i)].trim() == x['Correct Answer'].trim():
                        ans = answer.objects.create(question=qn, choice=c[i-1])
        else:
            file = request.FILES['file']
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
