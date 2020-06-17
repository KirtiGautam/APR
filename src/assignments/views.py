from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
import datetime
import json
from lessons.models import Subject, Lesson, question
from accounts.models import Class, pdf, video
from assignments.models import assignment, Pdf, Video, Test, Test_question

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
                Subject__Class=request.POST['id']):
            diff = x.Deadline-datetime.datetime.now(datetime.timezone.utc)
            deads.append({
                'assi': x,
                'days': diff.days,
                'hours': 24-datetime.datetime.now().hour,
                'minutes': 60-datetime.datetime.now().minute,
            })
        data = {
            'assignments': deads
        }
        client = {
            'body':  render_to_string('assignments/assignments.html', data),
        }
        return http.JsonResponse(client)
    else:
        http.HttpResponseForbidden({'message': 'Unauthorized'})


def assignmentDetail(request, id):
    if request.user.is_authenticated:
        data = {
            'assign': assignment.objects.get(id=id),
        }
        return render(request, 'assignments/assignmentDetailView.html', data)
    else:
        return redirect('accounts:login')


def vid(request, id):
    if request.user.is_authenticated:
        videos = Video.objects.get(id=id)
        return render(request, 'video/video.html', {'video': videos})
    else:
        return redirect('accounts:login')


def newAssignment(request):
    if request.user.is_authenticated:
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
    if request.user.is_authenticated:
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
