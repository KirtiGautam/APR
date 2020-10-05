from django.shortcuts import render, redirect
from django import http
from django.template.loader import render_to_string
from django.db.models import Q
from .models import (Post)


def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post.objects.create(
                Body=request.POST['body'], Owner=request.user)
            if 'photo' in request.FILES:
                post.Picture = request.FILES['photo']
                post.save()
            return http.JsonResponse(render_to_string('posts/post.html', {'posts': [post]}, request=request), safe=False)
        offset = int(request.GET['offset'])
        if request.user.admin:
            posts = Post.objects.all()
        elif request.user.is_staff:
            posts = Post.objects.filter(Q(Owner__admin=True) | Q(Owner__is_staff=True) | Q(
                Owner__Student__Class__Subject__in=request.user.teacher.all()))
        else:
            posts = Post.objects.filter(Q(Owner__admin=True) | Q(
                Owner__teacher__in=request.user.Student.Class.Subject.all()) | Q(Owner__Student__Class=request.user.Student.Class))
        return http.JsonResponse(render_to_string('posts/post.html', {'posts': posts.order_by('-Created')[offset*10:offset*10+10]}, request=request), safe=False)
    return http.HttpResponseForbidden("Not Allowed")
