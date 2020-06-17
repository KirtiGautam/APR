from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
import datetime
import json
from accounts.models import Class, pdf, video
from homework.models import homework, Pdf, Video, Test_question, Test
from lessons.models import Lesson, Subject, question


def homeworks(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name')
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
        }
        return http.JsonResponse(client)
    else:
        http.HttpResponseForbidden


def newHomework(request):
    if request.user.is_authenticated:
        home = homework.objects.get(id=1)
        # create(
        #     Name=request.POST['NOH'], Instructions=request.POST['instruction'], Subject=Subject.objects.get(id=request.POST['subject']))
        data = request.POST.getlist('data[]')
        if request.POST['type'] == 'pdf':
            for x in data:
                Pdf.objects.create(pdf=pdf.objects.get(id=x), lesson=Lesson.objects.get(
                    id=request.POST['lesson']), homework=home)
        elif request.POST['type'] == 'video':
            for x in data:
                Video.objects.create(video=video.objects.get(id=x), lesson=Lesson.objects.get(
                    id=request.POST['lesson']), homework=home)
        else:
            final = True if request.POST['final'] == '1' else False
            tes = Test.objects.create(Name=request.POST['TN'], Duration=request.POST['duration'],
                                      final=final, Homework=home)
            for x in data:
                Test_question.objects.create(
                    question=question.objects.get(id=x), test=tes)
        data = {
            'message': 'Data added'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Forbidden'})


def addresource(request):
    if request.user.is_authenticated:
        data = request.POST.getlist('data[]')
        if request.POST['type'] == 'pdf':
            for x in data:
                Pdf.objects.create(pdf=pdf.objects.get(id=x), lesson=Lesson.objects.get(
                    id=request.POST['lesson']), homework=homework.objects.get(id=request.POST['homework']))
        elif request.POST['type'] == 'video':
            for x in data:
                Video.objects.create(video=video.objects.get(id=x), lesson=Lesson.objects.get(
                    id=request.POST['lesson']), homework=homework.objects.get(id=request.POST['homework']))
        else:
            final = True if request.POST['final'] == '1' else False
            tes = Test.objects.create(Name=request.POST['Name'], Duration=request.POST['duration'],
                                      final=final, Homework=homework.objects.get(id=request.POST['homework']))
            for x in data:
                Test_question.objects.create(
                    question=question.objects.get(id=x), test=tes)
        return http.JsonResponse({'message': 'File uploaded'})
    return http.HttpResponseForbidden({'message': 'Forbidden'})


def getTest(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            data = {
                'test': Test.objects.get(id=id),
                'url': reverse('lessons:Test', args=[id]),
            }
            return render(request, 'test/test.html', data)
        else:
            Tes = Test.objects.get(id=id).question.all()
            correct = 0
            for x in Tes:
                if request.POST[str(x.id)] != '':
                    if int(request.POST[str(x.id)]) == x.question.Answer.choice.id:
                        correct += 1
            data = {
                'Number': Tes.count(),
                'Percentage': (correct/Tes.count())*100,
                'Correct': correct,
                'Wrong': Tes.count()-correct,
            }
            return render(request, 'test/result.html', data)
    else:
        return redirect('accounts:login')


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
        videos = Video.objects.get(id=id)
        return render(request, 'video/video.html', {'video': videos})
    else:
        return redirect('accounts:login')
