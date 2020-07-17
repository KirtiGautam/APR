from django.shortcuts import render, redirect, reverse
from django import http
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import default_storage
from lessons.models import Subject, Lesson, question
from accounts.models import Class, pdf, video, User
from assignments.models import assignment, Pdf, Video, Test, Test_question, user_progress_video, user_progress_pdf, AComment
from notifications.models import notifs
from django.utils import timezone, dateparse
import datetime
import json
import math


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
    if request.user.is_authenticated:
        if request.user.admin:
            return http.JsonResponse({
                'subjects': list(Subject.objects.filter(Class=request.POST['id']).values('id', 'Name')),
            })
        if request.user.is_staff:
            return http.JsonResponse({
                'subjects': list(request.user.teacher.filter(Class=request.POST['id']).values('id', 'Name')),
            })
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def getLessons(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
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
        elif request.user.is_staff:
            data = {
                'classes': request.user.teacher.all()
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
        if request.GET['time'] == 'present':
            if request.user.is_staff:
                rest = request.user.teacher.filter(Class=request.GET['id'])
            else:
                rest = Subject.objects.filter(Class=request.GET['id'])
            for x in assignment.objects.filter(Subject__in=rest, Deadline__gt=timezone.localtime()):
                diff = x.Deadline-timezone.localtime()
                user_watched = request.user.watched_assignment_video.filter(
                    Video__in=x.video.all()).count()
                user_read = request.user.read_assignment_pdf.filter(
                    Pdf__in=x.pdf.all()).count()
                total_pdf = x.pdf.all().count()
                total_video = x.video.all().count()
                deads.append({
                    'assi': x,
                    'days': diff.days,
                    'hours': diff.seconds//3600,
                    'minutes': (diff.seconds//60) % 60,
                    'progress': math.floor((sum([user_read, user_watched])/sum([total_pdf, total_video]) if sum([total_pdf, total_video]) > 0 else 1)*100),
                })
            data = {
                'assignments': deads,
            }
            client = {
                'body':  render_to_string('assignments/assignments.html', context=data, request=request),
            }
            return http.JsonResponse(client)
        else:
            if request.user.is_staff:
                rest = request.user.teacher.filter(Class=request.GET['id'])
            else:
                rest = Subject.objects.filter(Class=request.GET['id'])
            for x in assignment.objects.filter(
                    Subject__in=rest, Deadline__lt=timezone.localtime()):
                user_watched = request.user.watched_assignment_video.filter(
                    Video__in=x.video.all()).count()
                user_read = request.user.read_assignment_pdf.filter(
                    Pdf__in=x.pdf.all()).count()
                total_pdf = x.pdf.all().count()
                total_video = x.video.all().count()
                x.Deadline = x.Deadline.date()
                deads.append({
                    'assi': x,
                    'progress': math.floor((sum([user_read, user_watched])/sum([total_pdf, total_video]) if sum([total_pdf, total_video]) > 0 else 1)*100),
                })
            return render(request, 'assignments/past_assignments.html', {'assignments': deads})
    else:
        http.HttpResponseForbidden({'message': 'Unauthorized'})


def assignmentDetail(request, id):
    if request.user.is_authenticated:
        try:
            assign = assignment.objects.get(id=id)
        except assignment.DoesNotExist:
            return http.HttpResponseNotFound({'message': 'Not found'})
        if request.user.user_type == 'Student' and not assign.is_viewed(request.user):
            assign.viewed_by.add(request.user)
        data = {
            'assign': assign,
        }
        if assign.Deadline > datetime.datetime.now(datetime.timezone.utc):
            data['present'] = True
        else:
            data['present'] = False
        return render(request, 'assignments/assignmentDetailView.html', data)
    else:
        return redirect('accounts:login')


def vid(request, id):
    if request.user.is_authenticated:
        videos = Video.objects.get(id=id)
        if request.user.user_type == 'Student' and not videos.is_viewed(request.user):
            videos.viewed_by.add(request.user)
        next_video = videos.assignment.video.filter(id__gt=videos.id)
        if len(next_video) > 0:
            next_video = next_video[0]
            next = reverse('assignment:video', args=[next_video.id])
        else:
            next_video = None
            next = None
        done = True if request.user.watched_assignment_video.filter(
            Video=videos) else False
        data = {
            'next_video': next_video,
            'done': done,
            'video': videos,
            'next': next,
            'watched': reverse('assignment:mark_watched'),
        }
        return render(request, 'assignments/video.html', data)
    else:
        return redirect('accounts:login')


def newAssignment(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        dead = timezone.make_aware(
            dateparse.parse_datetime(request.POST['deadline']))
        subject = Subject.objects.get(id=request.POST['subject'])
        assign = assignment.objects.create(
            Name=request.POST['NOA'], Instructions=request.POST['instruction'], Deadline=dead, Subject=subject)

        # Notify users
        users = subject.Class.Students.all()
        link = reverse('assignment:assignmentDetails',
                       kwargs={'id': assign.id})
        message = 'New assignment added "'+assign.Name+'" for ' + assign.Subject.Name
        objs = [notifs(recipient=user.user, message=message, link=link)
                for user in users]
        notifs.objects.bulk_create(objs)
        data = {
            'message': 'Data added'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Forbidden'})


def addresource(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        data = request.POST.getlist('data[]')
        assign = assignment.objects.get(id=request.POST['assignment'])
        if request.POST['type'] == 'pdf':
            for x in data:
                Pdf.objects.create(pdf=pdf.objects.get(
                    id=x), lesson=Lesson.objects.get(id=request.POST['lesson']), assignment=assign)
        elif request.POST['type'] == 'video':
            for x in data:
                Video.objects.create(video=video.objects.get(
                    id=x), lesson=Lesson.objects.get(id=request.POST['lesson']), assignment=assign)
        else:
            final = True if request.POST['final'] == '1' else False
            tes = Test.objects.create(Name=request.POST['Name'], Duration=request.POST['duration'],
                                      final=final, Assignment=assign)
            for x in data:
                Test_question.objects.create(
                    question=question.objects.get(id=x), test=tes)
        # Notify users
        link = reverse('assignment:assignmentDetails',
                       kwargs={'id': assign.id})
        message = 'New '+request.POST['type']+' added in "' + \
            assign.Name+'" for ' + assign.Subject.Name
        objs = [notifs(recipient=user.user, message=message, link=link)
                for user in assign.Subject.Class.Students.all()]
        notifs.objects.bulk_create(objs)
        return http.JsonResponse({'message': 'File uploaded'})
    return http.HttpResponseForbidden({'message': 'Forbidden'})


def video_watched(request):
    if request.user.is_authenticated:
        if request.user.user_type == "Student":
            vid = Video.objects.get(id=request.POST['id'])
            if vid.assignment.Deadline < datetime.datetime.now(datetime.timezone.utc):
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
            if pd.assignment.Deadline < datetime.datetime.now(datetime.timezone.utc):
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


def AssignDetails(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        assign = assignment.objects.values(
            'id', 'Name', 'Instructions', 'Deadline').get(id=request.GET['id'])
        data = assign
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def updateDetails(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
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


def studentStats(request):
    if request.user.is_authenticated and (request.user.admin or request.user.is_staff):
        labels = []
        datac = []
        assign = assignment.objects.get(id=request.GET['id'])
        dat = []
        Total = sum([assign.pdf.all().count(), assign.video.all().count()])
        for x in assign.Subject.Class.Students.all():
            watched = x.user.watched_assignment_video.filter(
                Video__assignment=assign).count()
            read = x.user.read_assignment_pdf.filter(
                Pdf__assignment=assign).count()
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
            'assignment': assign,
            'students': dat,
            'Total': Total,
            'Pdf': assign.pdf.all().count(),
            'Video': assign.video.all().count(),
            'labels': labels,
            'data': datac
        }
        return render(request, 'assignments/studentStats.html', data)
    return redirect('accounts:login')


def assignmentComments(request):
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
                parent_obj = AComment.objects.get(id=parent_id)
            
            doubt = True if request.POST['doubt'] == 'true' else False

            AComment.objects.create(
                Video=Videos, Author=request.user, body=request.POST['body'], parent=parent_obj)

            # Send notifications if doubt
            if doubt:
                link = reverse('assignment:video', kwargs={'id': Videos.id})
                messsage = request.user.get_full_name()+' asked a doubt on lecture ' + \
                    Videos.video.Name
                admins = User.objects.filter(admin=True)
                teacher = Videos.assignment.Subject.teacher
                classmates = Videos.assignment.Subject.Class.Students.all().exclude(user=request.user)
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
        comment = AComment.objects.get(id=request.POST.get('id'))
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
        comment = AComment.objects.filter(id=request.POST['id'])
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
        comment = AComment.objects.get(id=request.POST['id'])
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
            AComment.objects.values(
                'body', 'id').get(id=request.GET['id'])
        )
    return http.HttpResponseForbidden({'message': 'Unauthorized'})


def newCount(request):
    if request.user.is_authenticated and request.user.user_type == 'Student':
        assign = assignment.objects.filter(Subject__Class=request.user.Student.Class).exclude(
            viewed_by__id=request.user.id).count()
        vids = Video.objects.filter(assignment__Subject__Class=request.user.Student.Class).exclude(
            viewed_by__id=request.user.id).count()
        pds = Pdf.objects.filter(assignment__Subject__Class=request.user.Student.Class).exclude(
            viewed_by__id=request.user.id).count()
        return http.JsonResponse({'new': (assign+vids+pds)})
    return http.JsonResponse({'message': 'Unauthorized'})
