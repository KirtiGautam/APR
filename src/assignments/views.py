from django.shortcuts import render, redirect
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
from accounts.models import Class
from assignments.models import assignment, pdf, video
from lessons.models import Subject, Lesson
import datetime


def getSubjects(request):
    if request.user.is_authenticated and request.user.admin:
        return http.JsonResponse({
            'subjects': list(Subject.objects.filter(Class=request.POST['id']).values('id', 'Name')),
        })
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def getLessons(request):
    if request.user.is_authenticated and request.user.admin:
        return http.JsonResponse({
            'lessons': list(Lesson.objects.filter(Subject=request.POST['id']).values('id', 'Name')),
        })
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def assignments(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name', 'section', 'year')
            }
            return render(request, 'assignments/assignment.html', data)
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
            'done': True
        }
        return http.JsonResponse(client)
    else:
        http.HttpResponseForbidden


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
        videos = video.objects.get(id=id)
        return render(request, 'video/video.html', {'video': videos})
    else:
        return redirect('accounts:login')


def newAssignment(request):
    if request.user.is_authenticated:
        assign = assignment.objects.create(
            Name=request.POST['Name'], Instructions=request.POST['instructions'], Deadline=request.POST['deadline'], Subject=Subject.objects.get(id=request.POST['subject']))
        File = request.POST['name']
        if request.POST['type'] == 'video':
            file = request.FILES['file']
            vid = video.objects.create(
                Name=File, platform='L', assignment=assign, lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save(
                'assignments/videos/'+str(vid.id)+'.mp4', file)
            vid.file = file_name
            vid.save()
        elif request.POST['type'] == 'csv':
            print(request.POST['file'])
        else:
            file = request.FILES['file']
            pd = pdf.objects.create(
                Name=File, assignment=assign, lesson=Lesson.objects.get(id=request.POST['lesson']))
            file_name = default_storage.save(
                'assignments/pdfs/'+str(pd.id)+'.pdf', file)
            pd.file = file_name
            pd.save()
        return http.JsonResponse({'message': True})
    return http.HttpResponseForbidden({'message': 'Forbidden'})
