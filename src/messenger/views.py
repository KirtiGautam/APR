from django.shortcuts import render, redirect
from django import http
from django.db.models import Q
from django.template.loader import render_to_string
from accounts.models import (User)
from messenger.models import (
    Message, MessageRecipient, Group, MessageRecipient)
import datetime


def index(request):
    if request.user.is_authenticated:
        data = {}
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
    return http.HttpResponseForbidden("Not alloewed")


def startChat(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.GET['id'])
        status = 'Online' if (datetime.datetime.now(datetime.timezone.utc) -
                              user.last_login).total_seconds() < 6 else 'Last seen at '+str(user.last_login.strftime("%d-%m-%Y %H:%M"))
        messages = Message.objects.filter((Q(Sender=request.user) & Q(Recipient__Recipient=user)) | (
            Q(Sender=user) & Q(Recipient__Recipient=request.user)), Recipient__Group__isnull=True)
        data = {
            'user': user.get_full_name(),
            'status': status,
            'messages': render_to_string('messenger/messages.html', {'messages': messages[0:20]}, request=request).replace('\n', ''),
        }
        MessageRecipient.objects.filter(
            Recipient=request.user, Message__in=messages).update(Read=True)
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not alloewed")


def newMessages(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.GET['id'])
        status = 'Online' if (datetime.datetime.now(datetime.timezone.utc) -
                              user.last_login).total_seconds() < 6 else 'Last seen at '+str(user.last_login.strftime("%d-%m-%Y %H:%M"))
        messages = Message.objects.filter((Q(Sender=user) & Q(
            Recipient__Recipient=request.user)), Recipient__Group__isnull=True, Recipient__Read=False)
        data = {
            'user': user.get_full_name(),
            'status': status,
            'messages': render_to_string('messenger/messages.html', {'messages': messages}, request=request).replace('\n', ''),
        }
        MessageRecipient.objects.filter(Message__in=messages).update(Read=True)
        return http.JsonResponse(data)


def newText(request):
    if request.user.is_authenticated:
        message = Message.objects.create(
            Sender=request.user, Body=request.POST['text'])
        MessageRecipient.objects.create(
            Message=message, Recipient=User.objects.get(id=request.POST['id']))
        data = {
            'message': render_to_string('messenger/messages.html', {'messages': [message]}, request=request).replace('\n', '')
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not alloewed")


def convos(request):
    if request.user.is_authenticated:
        user = request.user
        user.last_login = datetime.datetime.now(datetime.timezone.utc)
        user.save()
        messages = Message.objects.filter(Q(Sender=request.user) | Q(
            Recipient__Recipient=request.user), Recipient__Group__isnull=True).order_by('Created')
        conversations = {}
        for message in messages:
            if message.Sender == request.user:
                if message.Recipient.all().first().Recipient not in conversations:
                    conversations[message.Recipient.all(
                    ).first().Recipient.id] = message
            else:
                if message.Sender not in conversations:
                    conversations[message.Sender.id] = message
        # for key,conversation in conversations.items():
        #     print([key,conversation])
        data = {
            'body': render_to_string('messenger/history.html', {'conversations': conversations}, request=request)
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not alloewed")
