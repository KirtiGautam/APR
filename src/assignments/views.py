from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
import datetime
import json
from lessons.models import Subject, Lesson
from accounts.models import Class
from assignments.models import assignment

# def Test(request, id):
#     if request.user.is_authenticated:
#         if request.method == 'GET':
#             data = {
#                 'test': test.objects.get(id=id),
#                 'url': reverse('assignment:Test', args=[id]),
#             }
#             return render(request, 'test/test.html', data)
#         else:
#             Test = test.objects.get(id=id).question.all()
#             correct = 0
#             for x in Test:
#                 if request.POST[str(x.id)] != '':
#                     if int(request.POST[str(x.id)]) == x.Answer.choice.id:
#                         correct += 1
#             data = {
#                 'Number': Test.count(),
#                 'Percentage': (correct/Test.count())*100,
#                 'Correct': correct,
#                 'Wrong': Test.count()-correct,
#             }
#             return render(request, 'test/result.html', data)
#     return http.HttpResponseForbidden({'message': 'You are not authorized'})


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


# def assignmentDetail(request, id):
#     if request.user.is_authenticated:
#         data = {
#             'assign': assignment.objects.get(id=id),
#         }
#         return render(request, 'assignments/assignmentDetailView.html', data)
#     else:
#         return redirect('accounts:login')


# def vid(request, id):
#     if request.user.is_authenticated:
#         videos = video.objects.get(id=id)
#         return render(request, 'video/video.html', {'video': videos})
#     else:
#         return redirect('accounts:login')


# def newAssignment(request):
#     if request.user.is_authenticated:
#         assign = assignment.objects.create(
#             Name=request.POST['Name'], Instructions=request.POST['instructions'], Deadline=request.POST['deadline'], Subject=Subject.objects.get(id=request.POST['subject']))
#         File = request.POST['name']
#         if request.POST['type'] == 'video':
#             file = request.FILES['file']
#             vid = video.objects.create(
#                 Name=File, platform='L', assignment=assign, lesson=Lesson.objects.get(id=request.POST['lesson']))
#             file_name = default_storage.save(
#                 'assignments/videos/'+str(vid.id)+'.mp4', file)
#             vid.file = file_name
#             vid.save()
#         elif request.POST['type'] == 'csv':
#             Tobj = test.objects.create(
#                 Name=File, assignment=assign, Lesson=Lesson.objects.get(id=request.POST['lesson']))
#             for x in json.loads(request.POST['file']):
#                 qn = question.objects.create(Name=x['Question'], test=Tobj)
#                 c1 = choice.objects.create(
#                     Name=x['Choice 1'].strip(), question=qn)
#                 c2 = choice.objects.create(
#                     Name=x['Choice 2'].strip(), question=qn)
#                 c3 = choice.objects.create(
#                     Name=x['Choice 3'].strip(), question=qn)
#                 c4 = choice.objects.create(
#                     Name=x['Choice 4'].strip(), question=qn)
#                 c = [c1, c2, c3, c4]
#                 for i in range(1, 5):
#                     if x['Choice '+str(i)].strip() == x['Correct Answer'].strip():
#                         ans = answer.objects.create(question=qn, choice=c[i-1])
#         else:
#             file = request.FILES['file']
#             pd = pdf.objects.create(
#                 Name=File, assignment=assign, lesson=Lesson.objects.get(id=request.POST['lesson']))
#             file_name = default_storage.save(
#                 'assignments/pdfs/'+str(pd.id)+'.pdf', file)
#             pd.file = file_name
#             pd.save()
#         return http.JsonResponse({'message': True})
#     return http.HttpResponseForbidden({'message': 'Forbidden'})


# def addresource(request):
#     if request.user.is_authenticated:
#         assign = assignment.objects.get(id=request.POST['assignment'])
#         lesson = Lesson.objects.get(id=request.POST['lesson'])
#         if request.POST['type'] == 'video':
#             vid = video.objects.create(
#                 Name=request.POST['Name'], platform='L', lesson=lesson, assignment=assign)
#             file_name = default_storage.save(
#                 'assignments/videos/'+str(vid.id)+'.mp4', request.FILES['file'])
#             vid.file = file_name
#             vid.save()
#         elif request.POST['type'] == 'pdf':
#             pd = pdf.objects.create(
#                 Name=request.POST['Name'], assignment=assign, lesson=Lesson.objects.get(id=request.POST['lesson']))
#             file_name = default_storage.save(
#                 'assignments/pdfs/'+str(pd.id)+'.pdf', request.FILES['file'])
#             pd.file = file_name
#             pd.save()
#         else:
#             Tobj = test.objects.create(
#                 Name=request.POST['Name'], assignment=assign, Lesson=lesson)
#             for x in json.loads(request.POST['file']):
#                 qn = question.objects.create(Name=x['Question'], test=Tobj)
#                 c1 = choice.objects.create(
#                     Name=x['Choice 1'].strip(), question=qn)
#                 c2 = choice.objects.create(
#                     Name=x['Choice 2'].strip(), question=qn)
#                 c3 = choice.objects.create(
#                     Name=x['Choice 3'].strip(), question=qn)
#                 c4 = choice.objects.create(
#                     Name=x['Choice 4'].strip(), question=qn)
#                 c = [c1, c2, c3, c4]
#                 for i in range(1, 5):
#                     if x['Choice '+str(i)].strip() == x['Correct Answer'].strip():
#                         ans = answer.objects.create(question=qn, choice=c[i-1])
#         return http.JsonResponse({'message': 'File uploaded'})
#     return http.HttpResponseForbidden({'message': 'Forbidden'})
