from django.shortcuts import render, redirect
from django import http
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.models import (User, Class)
from messenger.models import (
    Message, MessageRecipient, Group, MessageRecipient, UserGroup, Announcement)
import datetime


def index(request):
    if request.user.is_authenticated:
        data = {}
        if 'type' in request.GET and request.GET['type'] == 'A':
            if request.user.admin:
                data = {
                    'users': User.objects.all(),
                    'Class': Class.objects.all(),
                }
            return render(request, 'messenger/announcement.html', data)
        return render(request, 'messenger/index.html', data)
    return redirect('accounts:login')


def getUsers(request):
    if request.user.is_authenticated:
        if request.user.admin:
            data = {
                'users': [{'id': user.id, 'name': user.get_full_name()} for user in User.objects.filter(status='A', first_name__icontains=request.GET['q']).exclude(id=request.user.id)]
            }
        elif request.user.is_staff:
            users = [{'id': user.id, 'name': user.get_full_name()} for user in User.objects.filter(
                status='A', Student__Class__in=request.user.teacher.Class.all(), first_name__icontains=request.GET['q'])]
            for user in User.objects.filter(status='A', is_staff=True, first_name__icontains=request.GET['q']).exclude(id=request.user.id):
                users.append({'id': user.id, 'name': user.get_full_name()})
            for user in User.objects.filter(status='A', admin=True, first_name__icontains=request.GET['q']):
                users.append({'id': user.id, 'name': user.get_full_name()})
            data = {
                'users': users
            }
        else:
            users = [{'id': user.id, 'name': user.get_full_name(
            )} for user in User.objects.filter(teacher__in=request.user.Student.Class.Subject.all(), first_name__icontains=request.GET['q'], status='A')]
            for user in User.objects.filter(Student__Class=request.user.Student.Class, first_name__icontains=request.GET['q'], status='A').exclude(id=request.user.id):
                users.append({'id': user.id, 'name': user.get_full_name()})
            for user in User.objects.filter(admin=True, first_name__icontains=request.GET['q'], status='A'):
                users.append({'id': user.id, 'name': user.get_full_name()})
            data = {
                'users': users
            }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not allowed")


def startChat(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            group = Group.objects.create(Name=request.POST['name'])
            UserGroup.objects.bulk_create([UserGroup(User=User.objects.get(
                id=x), Group=group) for x in request.POST.getlist('selected[]')])
            UserGroup.objects.create(Group=group, User=request.user)
            message = Message.objects.create(
                Sender=request.user, Body=request.POST['text'])
            MessageRecipient.objects.bulk_create([MessageRecipient(
                Message=message, Group=group, Recipient=User.objects.get(id=x)) for x in request.POST.getlist('selected[]')])
            data = {
                'group': group.id,
                'name': group.Name,
                'messages': render_to_string('messenger/messages.html', {'messages': [message]}, request=request)
            }
            return http.JsonResponse(data)
        if 'type' in request.GET:
            group = Group.objects.get(id=request.GET['id'])
            messages = Message.objects.filter(Q(Sender=request.user) | Q(
                Recipient__Recipient=request.user), Recipient__Group=group).distinct().order_by('-Created')
            data = {
                'group': group.id,
                'name': group.Name,
                'messages': render_to_string('messenger/messages.html', {'messages': reversed(messages[0:20])}, request=request),
            }
            MessageRecipient.objects.filter(
                Recipient=request.user, Message__in=messages).update(Read=True)
            return http.JsonResponse(data)
        else:
            user = User.objects.get(id=request.GET['id'])
            status = 'Online' if (datetime.datetime.now(datetime.timezone.utc) -
                                  user.last_login).total_seconds() < 6 else 'Last seen at '+str(user.last_login.strftime("%d-%m-%Y %H:%M"))
            messages = Message.objects.filter((Q(Sender=request.user) & Q(Recipient__Recipient=user)) | (
                Q(Sender=user) & Q(Recipient__Recipient=request.user)), Recipient__Group__isnull=True).order_by('-Created')
            data = {
                'user': user.get_full_name(),
                'status': status,
                'messages': render_to_string('messenger/messages.html', {'messages': reversed(messages[0:20])}, request=request),
            }
            MessageRecipient.objects.filter(
                Recipient=request.user, Message__in=messages).update(Read=True)
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not allowed")


def newMessages(request):
    if request.user.is_authenticated:
        if 'type' in request.GET:
            group = Group.objects.get(id=request.GET['id'])
            messages = Message.objects.filter(
                Recipient__Recipient=request.user, Recipient__Group=group, Recipient__Read=False)
            data = {
                'name': group.Name,
                'messages': render_to_string('messenger/messages.html', {'messages': messages}, request=request),
            }
        else:
            user = User.objects.get(id=request.GET['id'])
            status = 'Online' if (datetime.datetime.now(datetime.timezone.utc) -
                                  user.last_login).total_seconds() < 6 else 'Last seen at '+str(user.last_login.strftime("%d-%m-%Y %H:%M"))
            messages = Message.objects.filter((Q(Sender=user) & Q(
                Recipient__Recipient=request.user)), Recipient__Group__isnull=True, Recipient__Read=False)
            data = {
                'user': user.get_full_name(),
                'status': status,
                'messages': render_to_string('messenger/messages.html', {'messages': messages}, request=request),
            }
        MessageRecipient.objects.filter(Message__in=messages).update(Read=True)
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not allowed")


def newText(request):
    if request.user.is_authenticated:
        message = Message.objects.create(
            Sender=request.user, Body=request.POST['text'])
        if 'type' in request.POST:
            users = User.objects.filter(
                Group__Group=request.POST['id']).exclude(id=request.user.id)
            group = Group.objects.get(id=request.POST['id'])
            MessageRecipient.objects.bulk_create(
                [MessageRecipient(Message=message, Recipient=x, Group=group) for x in users])
        else:
            MessageRecipient.objects.create(
                Message=message, Recipient=User.objects.get(id=request.POST['id']))
        data = {
            'message': render_to_string('messenger/messages.html', {'messages': [message]}, request=request)
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not allowed")


def convos(request):
    if request.user.is_authenticated:
        user = request.user
        user.last_login = datetime.datetime.now(datetime.timezone.utc)
        user.save()
        conversations = {}
        if 'type' in request.GET:
            groups = Group.objects.filter(Users__User=user)
            messages = Message.objects.filter((Q(Sender=user) | Q(
                Recipient__Recipient=user)), Recipient__Group__in=groups).order_by('-Created')
            for message in messages:
                if message.Recipient.all().first().Group.id not in conversations:
                    conversations[message.Recipient.all(
                    ).first().Group.id] = message
            renderData = {'conversations': conversations, 'group': True}
        else:
            messages = Message.objects.filter(Q(Sender=request.user) | Q(
                Recipient__Recipient=request.user), Recipient__Group__isnull=True).order_by('-Created')
            for message in messages:
                if message.Sender == request.user:
                    if message.Recipient.all().first().Recipient not in conversations:
                        conversations[message.Recipient.all(
                        ).first().Recipient.id] = message
                else:
                    if message.Sender not in conversations:
                        conversations[message.Sender.id] = message
            renderData = {'conversations': conversations, 'group': False}
        data = {
            'body': render_to_string('messenger/history.html', renderData, request=request)
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not allowed")


def announcements(request):
    if request.user.is_authenticated:
        anns = request.user.announcement.all()
        data = [{
            'id': x.id,
            'Title': x.Title,
            'Message': x.Message,
            'Created': x.when(),
        } for x in anns.order_by('-Created')]
        return http.JsonResponse(data, safe=False)
    return http.HttpResponseForbidden("Not allowed")


def makeAnnouncement(request):
    if request.user.is_authenticated and request.user.admin:
        # <QueryDict: {'group[]': ['S'], 'Media[]': ['W'], 'title': ['Hey']}>
        users = []
        for x in request.POST.getlist('group[]'):
            if x == 'S':
                for y in User.objects.filter(user_type='Student'):
                    users.append(y)
            if x == 'T':
                for y in User.objects.filter(is_staff=True):
                    users.append(y)
        for x in request.POST.getlist('individual[]'):
            if x not in users:
                users.append(User.objects.get(id=x))
        for x in User.objects.filter(Student__Class__in=request.POST.getlist('Class[]'), status='A'):
            if x not in users:
                users.append(x)
        print(users)
        print(request.POST)
        Announcement.objects.create(
            Message=request.POST['text'], Recipient=request.user, Title=request.POST['title'])
        for x in request.POST.getlist('Media[]'):
            if x == 'W':
                Announcement.objects.bulk_create([Announcement(
                    Message=request.POST['text'], Recipient=x, Title=request.POST['title']) for x in users])
                print(x)
            if x == 'E':
                from django.core import mail
                connection = mail.get_connection()
                for x in users:
                    mail.send_mail(
                        subject=request.POST['title'],
                        from_email='Akshara <noreply@akshara.ubiqe.in>',
                        message=strip_tags(request.POST['text']),
                        html_message=request.POST['text'],
                        recipient_list=users,
                        fail_silently=True,
                        connection=connection)
        data = {
            'done': True
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not allowed")
