from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import User, Class


def student_information(request):
    if request.user.is_authenticated and request.user.admin:
        data = {
            'classes': Class.objects.all()
        }
        return render(request, 'settings/admin/studentinfo/studentInfo.html', data)
    return redirect('accounts:dashboard')

def school_staff(request):
    if request.user.is_authenticated and request.user.admin:
        return render(request, 'settings/admin/schoolStaff/schoolStaff.html')
    return redirect('accounts:dashboard')


def log(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            context = {
                'failed': True,
            }
            return render(request, 'login.html', context)
    else:
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        else:
            context = {
                'failed': False,
            }
            return render(request, 'login.html', context)


def logo(request):
    logout(request)
    return redirect('accounts:login')


def index(request):
    if request.user.is_authenticated:
        return render(request, 'home/dashboard.html')
    else:
        return redirect('accounts:login')
