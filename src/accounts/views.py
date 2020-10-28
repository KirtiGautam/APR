from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import User, Class, Student
from django import http
from django.contrib import messages


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            user.avatar = request.FILES['dp']
            user.save()
            return http.JsonResponse(user.avatar.url, safe=False)
        return render(request, 'settings/user/profile.html')
    return redirect('accounts:login')


def classes(request):
    if request.user.is_authenticated and request.user.admin:
        data = {
            'classes': Class.objects.all(),
            'teachers': User.objects.filter(is_staff=True)
        }
        return render(request, 'settings/admin/classes/classes.html', data)
    return redirect('accounts:dashboard')


def chapters(request):
    if request.user.is_authenticated and request.user.admin:
        data = {
            'classes': Class.objects.all()
        }
        return render(request, 'settings/admin/Chapters/chapters.html', data)
    return redirect('accounts:dashboard')


def student_information(request):
    if request.user.is_authenticated and request.user.admin:
        data = {
            'classes': Class.objects.all(),
            'pending': Student.objects.filter(user__status='P').count()
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
        if user is not None and user.status == 'A':
            if hasattr(user, 'logged_in_user'):
                messages.warning(
                    request, 'You have been logged out of other devices')
            login(request, user)
            return redirect('accounts:dashboard')
        elif user is not None and user.status == 'P':
            context = {
                'failed': True,
                'message': 'Your account is pending confirmation from Admin'
            }
        else:
            context = {
                'failed': True,
                'message': 'Invalid Credentials'
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
        # return redirect('lessons:lessons')
        return render(request, 'home/dashboard.html')
    else:
        return redirect('accounts:login')


def signupForm(request):
    if request.user.is_authenticated:
        return redirect('accounts:login')
    if request.session.get('temp_user', None) == '@uthenticated':
        if request.method == 'GET':
            classes = Class.objects.all()
            users = User.objects.all().values('email')
            data = {
                'Classes': classes,
                'emails': users,
            }
            return render(request, 'signupform.html', data)
        else:
            user = User.objects.create_user(
                email=request.POST['email'],
                password=(request.POST['Contact']).strip(),
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                status='P',
                user_type='Student'
            )
            try:
                student = Student.objects.create(
                    user=user,
                    gender=request.POST['gender'],
                    Contact=request.POST['Contact'],
                    dob=request.POST['dob'],
                    Address=request.POST['Address'],
                    City=request.POST['City'],
                    District=request.POST['District'],
                    State=request.POST['State'],
                    Pincode=request.POST['Pincode'],
                    Class=Class.objects.get(id=request.POST['Class'])
                )
            except Exception as e:
                user.delete()
                del request.session['temp_user']
                return http.JsonResponse(e.args, safe=False)
            del request.session['temp_user']
            return render(request, 'Thanks.html', {'student': student})
    return redirect('accounts:signup')


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:login')
    if request.session.get('temp_user', None) == '@uthenticated':
        return redirect('accounts:signup_form')
    if request.method == 'POST':
        password = "20vij001akshara"
        result = request.POST['sign_up']
        if password == result:
            request.session['temp_user'] = '@uthenticated'
        return redirect('accounts:signup_form')
    return render(request, 'signup.html')
