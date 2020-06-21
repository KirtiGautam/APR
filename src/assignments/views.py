from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
import datetime
import json
import math
from lessons.models import Subject, Lesson, question
from accounts.models import Class, pdf, video
from assignments.models import assignment, Pdf, Video, Test, Test_question, user_progress_video, user_progress_pdf


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


def getSubjects(request):
    if request.user.is_authenticated and request.user.admin:
        return http.JsonResponse({
            'subjects': list(Subject.objects.filter(Class=request.POST['id']).values('id', 'Name')),
        })
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def getLessons(request):
    if request.user.is_authenticated and request.user.admin:
        return http.JsonResponse({
            'lessons': list(Lesson.objects.filter(Subject=request.POST['id']).values('id', 'Name', 'Number')),
        })
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def assignments(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name')
            }
        else:
            data = {
                'class': request.user.Student.Class.id
            }
        return render(request, 'assignments/assignment.html', data)
    else:
        return redirect('accounts:login')


def getAssignments(request):
    if request.user.is_authenticated:
        deads = []
        for x in assignment.objects.filter(
                Subject__Class=request.POST['id'], Deadline__gt=datetime.datetime.now(datetime.timezone.utc)):
            diff = x.Deadline-datetime.datetime.now(datetime.timezone.utc)
            user_watched = request.user.watched_assignment_video.filter(
                Video__in=x.video.all()).count()
            user_read = request.user.read_assignment_pdf.filter(
                Pdf__in=x.pdf.all()).count()
            total_pdf = x.pdf.all().count()
            total_video = x.video.all().count()
            deads.append({
                'assi': x,
                'days': diff.days,
                'hours': 24-datetime.datetime.now(datetime.timezone.utc).hour,
                'minutes': 60-datetime.datetime.now(datetime.timezone.utc).minute,
                'progress': math.floor((sum([user_read, user_watched])/sum([total_pdf, total_video]))*100),
            })
        data = {
            'assignments': deads,
        }
        client = {
            'body':  render_to_string('assignments/assignments.html', context=data, request=request),
        }
        return http.JsonResponse(client)
    else:
        http.HttpResponseForbidden({'message': 'Unauthorized'})


def assignmentDetail(request, id):
    if request.user.is_authenticated:
        try:
            assign = assignment.objects.get(id=id)
        except assignment.DoesNotExist:
            return http.HttpResponseNotFound({'message': 'Not found'})
        if assign.Deadline > datetime.datetime.now(datetime.timezone.utc):
            data = {
                'assign': assign,
            }
            return render(request, 'assignments/assignmentDetailView.html', data)
        else:
            return redirect('assignment:assignments')
    else:
        return redirect('accounts:login')


def vid(request, id):
    if request.user.is_authenticated:
        videos = Video.objects.get(id=id)
        next = videos.assignment.video.filter(id__gt=videos.id)
        if len(next) > 0:
            next = reverse('assignment:video', args=[next[0].id])
        else:
            next = None
        data = {
            'video': videos,
            'next': next,
            'watched': reverse('assignment:mark_watched'),
        }
        return render(request, 'assignments/video.html', data)
    else:
        return redirect('accounts:login')


def newAssignment(request):
    if request.user.is_authenticated and request.user.admin:
        assi = assignment.objects.create(
            Name=request.POST['NOA'], Instructions=request.POST['instruction'], Deadline=request.POST['deadline'], Subject=Subject.objects.get(id=request.POST['subject']))
        data = request.POST.getlist('data[]')
        if request.POST['type'] == 'pdf':
            for x in data:
                Pdf.objects.create(pdf=pdf.objects.get(id=x), lesson=Lesson.objects.get(
                    id=request.POST['lesson']), assignment=assi)
        elif request.POST['type'] == 'video':
            for x in data:
                Video.objects.create(video=video.objects.get(id=x), lesson=Lesson.objects.get(
                    id=request.POST['lesson']), assignment=assi)
        else:
            final = True if request.POST['final'] == '1' else False
            tes = Test.objects.create(Name=request.POST['TN'], Duration=request.POST['duration'],
                                      final=final, Assignment=assi)
            for x in data:
                Test_question.objects.create(
                    question=question.objects.get(id=x), test=tes)
        data = {
            'message': 'Data added'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Forbidden'})


def addresource(request):
    if request.user.is_authenticated and request.user.admin:
        data = request.POST.getlist('data[]')
        if request.POST['type'] == 'pdf':
            for x in data:
                Pdf.objects.create(pdf=pdf.objects.get(
                    id=x), lesson=Lesson.objects.get(id=request.POST['lesson']), assignment=assignment.objects.get(id=request.POST['assignment']))
        elif request.POST['type'] == 'video':
            for x in data:
                Video.objects.create(video=video.objects.get(
                    id=x), lesson=Lesson.objects.get(id=request.POST['lesson']), assignment=assignment.objects.get(id=request.POST['assignment']))
        else:
            final = True if request.POST['final'] == '1' else False
            tes = Test.objects.create(Name=request.POST['Name'], Duration=request.POST['duration'],
                                      final=final, Assignment=assignment.objects.get(id=request.POST['assignment']))
            for x in data:
                Test_question.objects.create(
                    question=question.objects.get(id=x), test=tes)
        return http.JsonResponse({'message': 'File uploaded'})
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
                Video.objects.get(id=dat['value']).delete()
        data = {
            'message': 'Media deleted'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def AssignDetails(request):
    if request.user.is_authenticated and request.user.admin:
        assign = assignment.objects.values(
            'id', 'Name', 'Instructions', 'Deadline').get(id=request.GET['id'])
        data = assign
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def updateDetails(request):
    if request.user.is_authenticated and request.user.admin:
        assign = assignment.objects.get(id=request.POST['id'])
        assign.Name = request.POST['Name']
        assign.Instructions = request.POST['Instructions']
        assign.Deadline = request.POST['Deadline']
        assign.save()
        data = {
            'message': 'Details updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})
