from django.shortcuts import render, redirect
from accounts.models import pdf, video, Class
from lessons.models import Subject, Lesson, question, choice, answer
from django import http
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.conf import settings
import json


def delete_question(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        question.objects.filter(id__in=request.POST.getlist('data[]')).delete()
        data = {
            'message': 'Selected questions deleted successfully'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def get_question(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        ques = question.objects.get(id=request.GET['question'])
        data = {
            'Name': ques.Name,
            'choices': [{
                'id': c.id,
                'Name': c.Name
            }for c in ques.choice.all()],
            'Difficulty': ques.get_Difficulty_display(),
            'Answer': ques.Answer.choice.id,
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def edit_question(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        ques = question.objects.get(id=request.POST['question'])
        ques.Name = request.POST['Name']
        ques.Difficulty = request.POST['Difficulty']
        ques.save()
        for x in request.POST.getlist('choices[]'):
            c = json.loads(x)
            ch = choice.objects.get(id=c['id'])
            ch.Name = c['Name']
            ch.save()
        ans = ques.Answer
        ans.choice = choice.objects.get(id=request.POST['answer'])
        ans.save()
        data = {
            'message': 'Question updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def updateMedia(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        if request.POST['type'] == 'pdf':
            pd = pdf.objects.get(id=request.POST['id'])
            pd.Name = request.POST['Name']
            pd.Description = request.POST['Description']
            pd.save()
        else:
            vd = video.objects.get(id=request.POST['id'])
            vd.Name = request.POST['Name']
            vd.Description = request.POST['Description']
            vd.save()
        data = {
            'message': 'Details updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def mediaDetails(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        if request.POST['type'] == 'pdf':
            pd = pdf.objects.get(id=request.POST['value'])
            data = {
                'Name': pd.Name,
                'Description': pd.Description,
            }
        else:
            vd = video.objects.get(id=request.POST['value'])
            data = {
                'Name': vd.Name,
                'Description': vd.Description,
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def deleteMedia(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        for x in request.POST.getlist('data[]'):
            dat = json.loads(x)
            if dat['type'] == 'pdf':
                pd = pdf.objects.get(id=dat['value'])
                pd.file.delete()
                pd.delete()
            else:
                vd = video.objects.get(id=dat['value'])
                if vd.Local:
                    vd.file.delete()
                vd.delete()
        data = {
            'message': 'Files deleted'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def uploadQuestions(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        lesson = Lesson.objects.get(id=request.POST['lesson'])
        for x in json.loads(request.POST['file']):
            qn = question.objects.create(
                Name=x['Question'], Lesson=lesson, Difficulty=x['Difficulty'])
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
                if x['Choice '+str(i)].strip().lower() == x['Correct Answer'].strip().lower():
                    ans = answer.objects.create(
                        question=qn, choice=c[i-1], explanation=x['Explanation'])
        data = {
            'message': 'File uploaded'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def questions(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        data = {
            'class': Class.objects.all(),
            'question': question.objects.filter(Lesson__id=request.GET['lesson']),
        }
        return render(request, 'settings/admin/Allquestions/allquestions.html', data)
    return redirect('accounts:dashboard')


def allquestions(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        data = {
            'class': Class.objects.all()
        }
        return render(request, 'settings/admin/Allquestions/allquestions.html', data)
    return redirect('accounts:dashboard')


def allmedia(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        return render(request, 'settings/admin/AllMedia/allmedia.html')
    return redirect('accounts:dashboard')


def upload(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        if request.POST['dataType'] == 'pdf':
            file = request.FILES['file']
            fs = FileSystemStorage()
            name = fs.save('pdfs/'+file.name.replace(" ", ""), file)
            pdf.objects.create(
                Name=request.POST['Name'], Description=request.POST['description'], file=name)
            data = {
                'url': fs.url(name),
                'message': 'Data uploaded'
            }
        elif request.POST['dataType'] == 'video':
            if request.POST['videoType'] == 'local':
                file = request.FILES['file']
                fs = FileSystemStorage()
                name = fs.save('videos/'+file.name.replace(" ", ""), file)
                video.objects.create(
                    Name=request.POST['Name'], Description=request.POST['description'], file=name)
                data = {
                    'url': fs.url(name)
                }
            if request.POST['videoType'] == 'youtube':
                file = request.POST['file']
                video.objects.create(
                    Name=request.POST['Name'], Description=request.POST['description'], file=file, Local=False)
                data = {
                    'url': file
                }
            data['message'] = 'Data uploaded'
        else:
            data = {
                'message': 'Undefined Media type uploaded'
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def getMedia(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        if request.GET['type'] == 'video':
            vids = video.objects.filter(Name__contains=request.GET['term']).values('id', 'Name', 'Description',
                                                                                   'Local', 'file').order_by('-created')
            data = {
                'video': list(vids)
            }
        elif request.GET['type'] == 'pdf':
            pds = pdf.objects.filter(Name__contains=request.GET['term']).values(
                'id', 'Name', 'Description', 'file').order_by('-created')
            data = {
                'pdf': list(pds)
            }
        else:
            vids = video.objects.filter(Name__contains=request.GET['term']).values('id', 'Name', 'Description',
                                                                                   'Local', 'file').order_by('-created')
            pds = pdf.objects.filter(Name__contains=request.GET['term']).values(
                'id', 'Name', 'Description', 'file').order_by('-created')
            data = {
                'video': list(vids),
                'pdf': list(pds)
            }
        data['prefix'] = settings.MEDIA_URL
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})
