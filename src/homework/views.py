from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
from accounts.models import Class
from homework.models import homework, pdf, video, test, question, choice, answer
from lessons.models import Lesson, Subject
import datetime, json


def newHomework(request):
    if request.user.is_authenticated:
        home = homework.objects.create(
            Name=request.POST['Name'], Instructions=request.POST['instructions'], Subject=Subject.objects.get(id=request.POST['subject']))
        File = request.POST['name']
        if request.POST['type'] == 'video':
            file = request.FILES['file']
            vid = video.objects.create(
                Name=File, platform='L', homework=home, lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save(
                'assignments/videos/'+str(vid.id)+'.mp4', file)
            vid.file = file_name
            vid.save()
        elif request.POST['type'] == 'csv':
            Tobj = test.objects.create(
                Name=File, homework=home, Lesson=Lesson.objects.get(id=request.POST['lesson']))
            for x in json.loads(request.POST['file']):
                qn = question.objects.create(Name=x['Question'], test=Tobj)
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
                    if x['Choice '+str(i)].strip() == x['Correct Answer'].strip():
                        ans = answer.objects.create(question=qn, choice=c[i-1])
        else:
            file = request.FILES['file']
            pd = pdf.objects.create(
                Name=File, homework=home, lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save(
                'assignments/pdfs/'+str(pd.id)+'.pdf', file)
            pd.file = file_name
            pd.save()
        return http.JsonResponse({'message': 'File uploaded'})
    return http.HttpResponseForbidden({'message': 'Forbidden'})


def addresource(request):
    if request.user.is_authenticated:
        home = homework.objects.get(id=request.POST['homework'])
        lesson = Lesson.objects.get(id=request.POST['lesson'])
        if request.POST['type'] == 'video':
            vid = video.objects.create(
                Name=request.POST['Name'], platform='L', lesson=lesson, homework=home)
            file_name = default_storage.save(
                'assignments/videos/'+str(vid.id)+'.mp4', request.FILES['file'])
            vid.file = file_name
            vid.save()
        elif request.POST['type'] == 'pdf':
            pd = pdf.objects.create(
                Name=request.POST['Name'], homework=home, lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save(
                'assignments/pdfs/'+str(pd.id)+'.pdf', request.FILES['file'])
            pd.file = file_name
            pd.save()
        else:
            Tobj = test.objects.create(
                Name=request.POST['Name'], homework=home, Lesson=lesson)
            for x in json.loads(request.POST['file']):
                qn = question.objects.create(Name=x['Question'], test=Tobj)
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
                    if x['Choice '+str(i)].strip() == x['Correct Answer'].strip():
                        ans = answer.objects.create(question=qn, choice=c[i-1])
        return http.JsonResponse({'message': 'File uploaded'})
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def Test(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            data = {
                'test': test.objects.get(id=id),
                'url': reverse('homework:Test', args=[id]),
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
    return http.HttpResponseForbidden({'message': 'You are not authorized'})


def homeworks(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name', 'section', 'year')
            }
        else:
            data = {
                'class': request.user.Student.Class.id
            }
        return render(request, 'homeworks/homework.html', data)
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
