from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
import json
from accounts.models import Class, video, pdf
from lessons.models import Subject, question, Pdf, Video, Lesson, Test, Test_question


def getQuestions(request):
    if request.user.admin and request.user.is_authenticated:
        questions = question.objects.filter(
            Lesson=request.POST['lesson']).values('id', 'Name', 'Difficulty')
        data = {
            'questions': list(questions)
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


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


def lessons(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name')
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
        videos = Video.objects.get(id=id)
        return render(request, 'video/video.html', {'video': videos})
    else:
        return redirect('accounts:login')


def addResource(request):
    if request.user.is_authenticated and request.user.admin:
        data = request.POST.getlist('data[]')
        if request.POST['type'] == 'pdf':
            for x in data:
                Pdf.objects.create(pdf=pdf.objects.get(
                    id=x), lesson=Lesson.objects.get(id=request.POST['lesson']))
        elif request.POST['type'] == 'video':
            for x in data:
                Video.objects.create(video=video.objects.get(
                    id=x), lesson=Lesson.objects.get(id=request.POST['lesson']))
        else:
            final = True if request.POST['final'] == '1' else False
            tes = Test.objects.create(Name=request.POST['Name'], Duration=request.POST['duration'],
                                      final=final, Lesson=Lesson.objects.get(id=request.POST['lesson']))
            for x in data:
                Test_question.objects.create(
                    question=question.objects.get(id=x), test=tes)
        data = {
            'message': 'Data added'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Forbidden'})
