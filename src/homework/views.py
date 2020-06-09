from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import Class
from homework.models import homework, pdf, video, test, question, choice, answer
import datetime


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
