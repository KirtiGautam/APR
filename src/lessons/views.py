from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
import json
import math
from accounts.models import Class, video, pdf
from lessons.models import Subject, question, Pdf, Video, Lesson, Test, Test_question, user_progress_pdf, user_progress_video


def getQuestions(request):
    if request.user.admin and request.user.is_authenticated:
        questions = question.objects.filter(
            Lesson=request.POST['lesson'])
        data = {
            'questions': [{
                'id': ques.id,
                'Name': ques.Name,
                'Difficulty': ques.get_Difficulty_display()
            } for ques in questions]
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
                'watched_videos': request.user.watched_lesson_video.all(),
                'read_pdfs': request.user.read_lesson_pdf.all(),
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
        next = videos.lesson.lesson_videos.filter(id__gt=videos.id)
        if len(next) > 0:
            next = reverse('lessons:video', args=[next[0].id])
        else:
            next = None
        data = {
            'video': videos,
            'next': next,
            'watched': reverse('lessons:mark_watched'),
        }
        return render(request, 'lesson/video.html', data)
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


def video_watched(request):
    if request.user.is_authenticated:
        progress, created = user_progress_video.objects.get_or_create(
            User=request.user, Video=Video.objects.get(id=request.POST['id']))
        if created:
            data = {
                'message': 'Video marked as watched successfully!'
            }
        else:
            data = {
                'message': 'Video already watched'
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def pdf_read(request):
    if request.user.is_authenticated:
        progress, created = user_progress_pdf.objects.get_or_create(
            User=request.user, Pdf=Pdf.objects.get(id=request.POST['id']))
        if created:
            data = {
                'message': 'Pdf marked as read successfully!'
            }
        else:
            data = {
                'message': 'Pdf already read'
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def deleteMedia(request):
    if request.user.is_authenticated and request.user.admin:
        for x in request.POST.getlist('data[]'):
            dat = json.loads(x)
            if dat['type'] == 'pdf':
                Pdf.objects.get(id=dat['value']).delete()
            else:
                vd = Video.objects.get(id=dat['value']).delete()
        data = {
            'message': 'Files deleted'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def studentStats(request):
    if request.user.is_authenticated and request.user.admin:
        labels = []
        datac = []
        lesson = Lesson.objects.get(id=request.GET['id'])
        dat = []
        Total = sum([lesson.lesson_pdfs.all().count(), lesson.lesson_videos.all().count()])
        for x in lesson.Subject.Class.Students.all():
            watched = x.user.watched_lesson_video.filter(Video__lesson=lesson).all().count()
            read = x.user.read_lesson_pdf.filter(Pdf__lesson=lesson).all().count()
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
            'lesson': lesson,
            'students': dat,
            'Total': Total,
            'Pdf': lesson.lesson_pdfs.all().count(),
            'Video': lesson.lesson_videos.all().count(),
            'labels': labels,
            'data': datac
        }
        return render(request, 'lesson/studentStats.html', data)
    return redirect('accounts:login')
