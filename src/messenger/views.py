from django.shortcuts import render, redirect
from django import http


def index(request):
    if request.user.is_authenticated:
        data = {}
        return render(request, 'messenger/index.html', data)
    return redirect('accounts:login')
