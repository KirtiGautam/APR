from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
import json
import math
from notifications.models import notifs
from accounts.models import Class, video, pdf, User
from lessons.models import (Subject, question, Pdf, Video, Lesson,
                            Test, Test_question, user_progress_pdf, user_progress_video, Comment)


def getQuestions(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
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
        elif request.user.is_staff:
            data = {
                'classes': request.user.teacher.all()
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
        if not request.GET['subject']:
            subject = request.user.teacher.filter(
                Class=request.GET['id']) if request.user.is_staff else Subject.objects.filter(Class=request.GET['id'])
        else:
            subject = Subject.objects.filter(id=request.GET['subject'])
        if subject:
            data = {
                'lessons': subject[0].Lesson.all(),
                'prefix': settings.MEDIA_URL,
                'admin': request.user.admin or request.user.is_staff,
                'watched_videos': request.user.watched_lesson_video.all(),
                'read_pdfs': request.user.read_lesson_pdf.all(),
            }
        else:
            data = {}
        send = request.user.teacher.filter(
            Class=request.GET['id']) if request.user.is_staff else Subject.objects.filter(Class=request.GET['id'])
        send = [{
            'id': subj.id,
            'Name': subj.Name,
            'count': sum([Video.objects.filter(lesson__Subject=subj).exclude(viewed_by__id=request.user.id).count(), Pdf.objects.filter(lesson__Subject=subj).exclude(viewed_by__id=request.user.id).count()]),
        } for subj in send]
        client = {
            'body': render_to_string('lesson/lessons.html', data, request=request),
            'subjects': list(send)
        }
        return http.JsonResponse(client, safe=False)
    else:
        return http.HttpResponseForbidden({'messsage': 'You are not authorized for this request'})


def vid(request, id):
    if request.user.is_authenticated:
        videos = Video.objects.get(id=id)
        if request.user.user_type == 'Student' and not videos.is_viewed(request.user):
            videos.viewed_by.add(request.user)
        next_video = videos.lesson.lesson_videos.filter(id__gt=videos.id)
        if len(next_video) > 0:
            next_video = next_video[0]
            next = reverse('lessons:video', args=[next_video.id])
        else:
            next_video = None
            next = None
        done = True if request.user.watched_lesson_video.filter(
            Video=videos) else False
        data = {
            'next_video': next_video,
            'done': done,
            'video': videos,
            'next': next,
            'watched': reverse('lessons:mark_watched'),
        }
        return render(request, 'lesson/video.html', data)
    else:
        return redirect('accounts:login')


def addResource(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        data = request.POST.getlist('data[]')
        lesson = Lesson.objects.get(id=request.POST['lesson'])
        if request.POST['type'] == 'pdf':
            for x in data:
                Pdf.objects.create(pdf=pdf.objects.get(
                    id=x), lesson=lesson)
        elif request.POST['type'] == 'video':
            for x in data:
                Video.objects.create(video=video.objects.get(
                    id=x), lesson=lesson)
        else:
            final = True if request.POST['final'] == '1' else False
            tes = Test.objects.create(Name=request.POST['Name'], Duration=request.POST['duration'],
                                      final=final, Lesson=lesson)
            for x in data:
                Test_question.objects.create(
                    question=question.objects.get(id=x), test=tes)

        # Notify users
        link = reverse('lessons:lessons')
        if request.POST['type'] == 'video':
            message = '<i class="fas fa-photo-video"></i> '
        elif request.POST['type'] == 'pdf':
            message = '<i class="fas fa-file-pdf"></i> '
        else:
            message = '<i class="fas fa-file-alt"></i> '
        message += 'New '+request.POSt['type']+' in "' + \
            lesson.Name+'" for ' + lesson.Subject.Name
        objs = [notifs(recipient=user.user, message=message, link=link)
                for user in lesson.Subject.Students.all()]
        notifs.objects.bulk_create(objs)
        data = {
            'message': 'Data added'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Forbidden'})


def video_watched(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Student':
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
        else:
            data = {
                'message': 'Only for students'
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def pdf_read(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Student':
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
                vd = Video.objects.get(id=dat['value']).delete()
        data = {
            'message': 'Files deleted'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def studentStats(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        labels = []
        datac = []
        lesson = Lesson.objects.get(id=request.GET['id'])
        dat = []
        Total = sum([lesson.lesson_pdfs.all().count(),
                     lesson.lesson_videos.all().count()])
        for x in lesson.Subject.Class.Students.all():
            watched = x.user.watched_lesson_video.filter(
                Video__lesson=lesson).all().count()
            read = x.user.read_lesson_pdf.filter(
                Pdf__lesson=lesson).all().count()
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


def lessonComments(request):
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
                parent_obj = Comment.objects.get(id=parent_id)

            doubt = True if request.POST['doubt'] == 'true' else False

            Comment.objects.create(
                Video=Videos, Author=request.user, body=request.POST['body'], doubt=doubt, parent=parent_obj)

            # Send notifications if doubt
            if doubt:
                link = reverse('lessons:video', kwargs={'id': Videos.id})
                messsage = '<i class="fas fa-question-circle"></i> ' + \
                    request.user.get_full_name()+' asked a doubt on lecture ' + Videos.video.Name
                admins = User.objects.filter(admin=True)
                teacher = Videos.lesson.Subject.teacher
                classmates = Videos.lesson.Subject.Class.Students.all().exclude(user=request.user)
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
        comment = Comment.objects.get(id=request.POST.get('id'))
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            if request.user.admin or request.user.is_staff:
                data = {
                    'message': 'Unappreciated'
                }
            else:
                data = {
                    'message': 'UnLiked'
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
        comment = Comment.objects.filter(id=request.POST['id'])
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
        comment = Comment.objects.get(id=request.POST['id'])
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
            Comment.objects.values(
                'body', 'id').get(id=request.GET['id'])
        )
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def newCount(request):
    if request.user.is_authenticated and request.user.user_type == 'Student':
        vids = Video.objects.filter(lesson__Subject__Class=request.user.Student.Class).exclude(
            viewed_by__id=request.user.id).count()
        pds = Pdf.objects.filter(lesson__Subject__Class=request.user.Student.Class).exclude(
            viewed_by__id=request.user.id).count()
        return http.JsonResponse({'new': (vids+pds)})
    return http.HttpResponseForbidden({'message': 'Unauthorized'})
