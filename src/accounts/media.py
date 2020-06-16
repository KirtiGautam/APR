from django.shortcuts import render, redirect
from accounts.models import pdf, video
from django import http
from django.core.files.storage import FileSystemStorage
from django.conf import settings


def allmedia(request):
    if request.user.is_authenticated and request.user.admin:
        return render(request, 'settings/admin/AllMedia/allmedia.html')
    return redirect('accounts:dashboard')


def upload(request):
    if request.user.is_authenticated and request.user.admin:
        if request.POST['dataType'] == 'pdf':
            file = request.FILES['file']
            fs = FileSystemStorage()
            name = fs.save('pdfs/'+file.name, file)
            pdf.objects.create(
                Name=request.POST['Name'], Description=request.POST['description'], file=name)
            data = {
                'url': fs.url(name)
            }
        elif request.POST['dataType'] == 'video':
            if request.POST['videoType'] == 'local':
                file = request.FILES['file']
                fs = FileSystemStorage()
                name = fs.save('videos/'+file.name, file)
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
        else:
            data = {
                'message': 'Undefined Media type uploaded'
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def getMedia(request):
    if request.user.is_authenticated and request.user.admin:
        if request.POST['type'] == 'video':
            data = {
                'video': list(video.objects.all().values('Name', 'Description', 'Local', 'file'))
            }
        elif request.POST['type'] == 'pdf':
            data = {
                'pdf': list(pdf.objects.all().values('Name', 'Description', 'file'))
            }
        else:
            data = {
                'video': list(video.objects.all().values('Name', 'Description', 'Local', 'file')),
                'pdf': list(pdf.objects.all().values('Name', 'Description', 'file'))
            }
        data['prefix'] = settings.MEDIA_URL
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})
