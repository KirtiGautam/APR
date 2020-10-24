from django.shortcuts import render
from django import http
from notifications.models import notifs
import datetime


def notifications(request):
    if request.user.is_authenticated:
        notifi = notifs.objects.filter(
            recipient=request.user).order_by('-recieved_date')
        data = {
            'notifications': [{
                'id': x.id,
                'message': x.message,
                'link': x.link,
                'read': x.read,
                'time': x.when(),
            }for x in notifi],
        }
        notifi.filter(recieved_date__lte=datetime.datetime.now(
            datetime.timezone.utc)-datetime.timedelta(days=7), read=True).delete()
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Forbidden'})


def read(request):
    if request.user.is_authenticated:
        notifi = notifs.objects.get(id=request.POST['id'])
        notifi.read = True
        notifi.save()
        data = {
            'message': 'Notification is read'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Forbidden'})
