from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
import datetime
import json
import math
from accounts.models import Class, pdf, video, User
from homework.models import homework, Pdf, Video, Test_question, Test, user_progress_video, user_progress_pdf, HComment
from lessons.models import Lesson, Subject, question
from notifications.models import notifs


def delhomework(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        home = homework.objects.get(id=request.POST['id'])
        home.delete()
        data = {
            'Message': 'Assignment Deleted'
        }
        return http.JsonResponse(data)
    return http.JsonResponse({'message': 'Unauthorized'})


def homeworks(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'classes': Class.objects.all().values('id', 'name')
            }
        elif request.user.is_staff:
            data = {
                'classes': request.user.teacher.all()
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
        if request.user.is_staff:
            subject = request.user.teacher.filter(Class=request.GET['id'])
        else:
            subject = Subject.objects.filter(Class=request.GET['id'])
        home = homework.objects.filter(
            Subject__in=subject, date=request.GET['date'])
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
        elif request.POST['type'] == 'test':
            final = True if request.POST['final'] == '1' else False
            tes = Test.objects.create(Name=request.POST['TN'], Duration=request.POST['duration'],
                                      final=final, Homework=home)
            for x in data:
                Test_question.objects.create(
                    question=question.objects.get(id=x), test=tes)

        # Notify users
        link = reverse('homework:homeworkDetails',
                       kwargs={'id': home.id})
        message = '<i class="fas fa-house-user"></i> New homework added <span class="font-weight-bold">"' + \
            home.Name+'"</span> for ' + home.Subject.Name
        objs = [notifs(recipient=user.user, message=message, link=link)
                for user in home.Subject.Class.Students.all()]
        notifs.objects.bulk_create(objs)
        data = {
            'message': 'Data added'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Forbidden'})


def addresource(request):
    if request.user.is_authenticated:
        data = request.POST.getlist('data[]')
        home = homework.objects.get(id=request.POST['homework'])
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
            tes = Test.objects.create(Name=request.POST['Name'], Duration=request.POST['duration'],
                                      final=final, Homework=home)
            for x in data:
                Test_question.objects.create(
                    question=question.objects.get(id=x), test=tes)

        # Notify users
        link = reverse('homework:homeworkDetails',
                       kwargs={'id': home.id})
        if request.POST['type'] == 'video':
            message = '<i class="fas fa-photo-video"></i> '
        elif request.POST['type'] == 'pdf':
            message = '<i class="fas fa-file-pdf"></i> '
        else:
            message = '<i class="fas fa-file-alt"></i> '
        message += 'New '+request.POST['type'] + ' added in <span class="font-weight-bold">"' + \
            home.Name+'"</span> for ' + home.Subject.Name
        objs = [notifs(recipient=user.user, message=message, link=link)
                for user in home.Subject.Class.Students.all()]
        notifs.objects.bulk_create(objs)
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
        try:
            homewrk = homework.objects.get(id=id)
        except homework.DoesNotExist:
            return http.HttpResponseNotFound({'message': 'Not found'})
        if request.user.user_type == 'Student' and not homewrk.is_viewed(request.user):
            homewrk.viewed_by.add(request.user)
        data = {
            'homework': homewrk,
            'prefix': settings.MEDIA_URL,
        }
        return render(request, 'homeworks/homeworkDetailView.html', data)
    else:
        return redirect('accounts:login')


def vid(request, id):
    if request.user.is_authenticated:
        videos = Video.objects.get(id=id)
        if request.user.user_type == 'Student' and not videos.is_viewed(request.user):
            videos.viewed_by.add(request.user)
        next_video = videos.homework.video.filter(id__gt=videos.id)
        if len(next_video) > 0:
            next_video = next_video[0]
            next = reverse('homework:video', args=[next_video.id])
        else:
            next_video = None
            next = None
        done = True if request.user.watched_homework_video.filter(
            Video=videos) else False
        data = {
            'next_video': next_video,
            'done': done,
            'video': videos,
            'next': next,
            'watched': reverse('homework:mark_watched'),
        }
        return render(request, 'homeworks/video.html', data)
    else:
        return redirect('accounts:login')


def video_watched(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Student':
            vid = Video.objects.get(id=request.POST['id'])
            if vid.homework.date < datetime.date.today():
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
                        'message': 'Video already watched',
                    }
                data['success'] = True
        else:
            data = {
                'message': 'Only for students'
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def pdf_read(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Student':
            pd = Pdf.objects.get(id=request.POST['id'])
            if pd.homework.date < datetime.date.today():
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
        else:
            data = {
                'message': 'Only for students'
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def deleteMedia(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
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
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        home = homework.objects.values(
            'id', 'Name', 'Instructions').get(id=request.GET['id'])
        data = home
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def updateDetails(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
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
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
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


def homeworkComments(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # get post object
            Videos = Video.objects.get(id=request.POST['id'])
            # comment has been added
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = HComment.objects.get(id=parent_id)

            doubt = True if request.POST['doubt'] == 'true' else False

            HComment.objects.create(
                Video=Videos, Author=request.user, body=request.POST['body'], parent=parent_obj)

            # Send notifications if doubt
            if doubt:
                link = reverse('homework:video', kwargs={'id': Videos.id})
                messsage = '<i class="fas fa-question-circle"></i> ' + \
                    request.user.get_full_name()+' asked a doubt on lecture ' + Videos.video.Name
                admins = User.objects.filter(admin=True)
                teacher = Videos.homework.Subject.teacher
                classmates = Videos.homework.Subject.Class.Students.all().exclude(user=request.user)
                notifs.objects.bulk_create(
                    [notifs(recipient=user, message=messsage, link=link) for user in admins])
                notifs.objects.create(
                    recipient=teacher, message=messsage, link=link)
                notifs.objects.bulk_create(
                    [notifs(recipient=user.user, message=messsage, link=link) for user in classmates])
        else:
            # get post object
            Videos = Video.objects.get(id=request.GET['id'])
        # list of active parent comments
        comments = Videos.comments.filter(
            parent__isnull=True).order_by('-created')
        # for x in comments:
        #     if x.likes.filter(id=request.user.id).exists():
        #         x['liked'] = True
        client = {
            'comments': comments
        }
        data = {
            'body': render_to_string('video/discussions.html', client, request=request)
        }
        return http.JsonResponse(data)


def likeComment(request):
    if request.user.is_authenticated:
        comment = HComment.objects.get(id=request.POST.get('id'))
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            if request.user.admin or request.user.is_staff:
                data = {
                    'message': 'Unappreciated'
                }
            else:
                data = {
                    'message': 'Unliked'
                }
        else:
            comment.likes.add(request.user)
            if request.user.admin or request.user.is_staff:
                data = {
                    'message': 'Appreciated'
                }
            else:
                data = {
                    'message': 'Liked'
                }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def deleteComment(request):
    if request.user.is_authenticated:
        comment = HComment.objects.filter(id=request.POST['id'])
        id = comment[0].id
        vid = comment[0].Video
        if request.user.user_type == "Student":
            if comment[0].Author != request.user:
                data = {
                    'message': "Cannot delete other user's comment"
                }
            else:
                comment.delete()
                data = {
                    'message': "Comment deleted"
                }
        else:
            comment.delete()
            data = {
                'message': "Comment deleted"
            }
        data['parent_id'] = id
        data['body'] = render_to_string('video/discussions.html', {'comments': Comment.objects.filter(
            Video=vid, parent__isnull=True)}, request=request)
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def updateComment(request):
    if request.user.is_authenticated:
        comment = HComment.objects.get(id=request.POST['id'])
        if 'resolved' in request.POST:
            comment.resolved = not comment.resolved
        else:
            comment.body = request.POST['body']
        comment.save()
        return http.JsonResponse({
            'message': 'Comment Updated'
        })
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def getComment(request):
    if request.user.is_authenticated:
        return http.JsonResponse(
            HComment.objects.values(
                'body', 'id').get(id=request.GET['id'])
        )
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def newCount(request):
    if request.user.is_authenticated and request.user.user_type == 'Student':
        homewrk = homework.objects.filter(Subject__Class=request.user.Student.Class).exclude(
            viewed_by__id=request.user.id).count()
        vids = Video.objects.filter(homework__Subject__Class=request.user.Student.Class).exclude(
            viewed_by__id=request.user.id).count()
        pds = Pdf.objects.filter(homework__Subject__Class=request.user.Student.Class).exclude(
            viewed_by__id=request.user.id).count()
        return http.JsonResponse({'new': (homewrk+vids+pds)})
    return http.JsonResponse({'message': 'Unauthorized'})
