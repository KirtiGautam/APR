from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
import datetime
import json
import math
from accounts.models import Class, pdf, video
from homework.models import homework, Pdf, Video, Test_question, Test, user_progress_video, user_progress_pdf
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
        home = homework.objects.filter(
            Subject__Class=request.POST['id'], date=request.POST['date'])
        data = {
            'homeworks': zip(home, [sum([request.user.watched_homework_video.filter(Video__in=x.video.all()).count(), request.user.read_homework_pdf.filter(Pdf__in=x.pdf.all()).count()]) for x in home]),
        }
        client = {
            'body':  render_to_string('homeworks/homeworks.html', context=data, request=request),
        }
        return http.JsonResponse(client)
    else:
        http.HttpResponseForbidden


def newHomework(request):
    if request.user.is_authenticated:
        home = homework.objects.create(
            Name=request.POST['NOH'], Instructions=request.POST['instruction'], Subject=Subject.objects.get(id=request.POST['subject']))
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
        next = videos.homework.video.filter(id__gt=videos.id)
        if len(next) > 0:
            next = reverse('homework:video', args=[next[0].id])
        else:
            next = None
        data = {
            'video': videos,
            'next': next,
            'watched': reverse('homework:mark_watched'),
        }
        return render(request, 'homeworks/video.html', data)
    else:
        return redirect('accounts:login')


def video_watched(request):
    if request.user.is_authenticated:
        vid = Video.objects.get(id=request.POST['id'])
        if vid.homework.Deadline < datetime.datetime.now(datetime.timezone.utc):
            data = {
                'message': 'Cannot submit after deadline',
                'success': False,
            }
        else:
            progress, created = user_progress_video.objects.get_or_create(
                User=request.user, Video=vid)
            if created:
                data = {
                    'message': 'Video marked as watched successfully!',
                }
            else:
                data = {
                    'message': 'Vido already watched',
                }
            data['success'] = True
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def pdf_read(request):
    if request.user.is_authenticated:
        pd = Pdf.objects.get(id=request.POST['id'])
        if pd.homework.Deadline < datetime.datetime.now(datetime.timezone.utc):
            data = {
                'message': 'Cannot submit after deadline',
                'success': False
            }
        else:
            progress, created = user_progress_pdf.objects.get_or_create(
                User=request.user, Pdf=pd)
            if created:
                data = {
                    'message': 'Pdf marked as read successfully!'
                }
            else:
                data = {
                    'message': 'Pdf already read'
                }
            data['success'] = True
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def deleteMedia(request):
    if request.user.is_authenticated and request.user.admin:
        for x in request.POST.getlist('data[]'):
            dat = json.loads(x)
            if dat['type'] == 'pdf':
                Pdf.objects.get(id=dat['value']).delete()
            else:
                Video.objects.get(id=dat['value']).delete()
        data = {
            'message': 'Media deleted'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def HomeDetails(request):
    if request.user.is_authenticated and request.user.admin:
        home = homework.objects.values(
            'id', 'Name', 'Instructions').get(id=request.GET['id'])
        data = home
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def updateDetails(request):
    if request.user.is_authenticated and request.user.admin:
        home = homework.objects.get(id=request.POST['id'])
        home.Name = request.POST['Name']
        home.Instructions = request.POST['Instructions']
        home.save()
        data = {
            'message': 'Details updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def studentStats(request):
    if request.user.is_authenticated and request.user.admin:
        home = homework.objects.get(id=request.GET['id'])
        labels = []
        datac = []
        dat = []
        Total = sum([home.pdf.all().count(), home.video.all().count()])
        for x in home.Subject.Class.Students.all():
            watched = x.user.watched_homework_video.filter(
                Video__homework=home).count()
            read = x.user.read_homework_pdf.filter(Pdf__homework=home).count()
            total = watched+read
            labels.append(x.user.get_full_name())
            datac.append(math.floor((total/Total if Total > 0 else 1)*100))
            dat.append({
                'Name': x.user.get_full_name(),
                'Completed_videos': watched,
                'Completed_pdfs': read,
                'Total': total,
                'percentage': math.floor((total/Total if Total > 0 else 1)*100)
            })
        data = {
            'homework': home,
            'students': dat,
            'Total': Total,
            'Pdf': home.pdf.all().count(),
            'Video': home.video.all().count(),
            'labels': labels,
            'data': datac
        }
        return render(request, 'homeworks/studentStats.html', data)
    return redirect('accounts:login')
