from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.models import User
from security.models import PasswordToken
from django.contrib import messages
import datetime
import uuid


def index(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if not user.exists():
            print(request.POST)
            messages.error(request, "No such Email")
            return redirect('security:index')
        user = user[0]
        if hasattr(user, 'ResetToken') and user.ResetToken.Expiration >= datetime.datetime.now(datetime.timezone.utc):
            messages.error(request, "Email already sent")
            return redirect('security:index')
        else:
            if hasattr(user, 'ResetToken'):
                user.ResetToken.delete()
            expiration = datetime.datetime.now(
                datetime.timezone.utc)+datetime.timedelta(minutes=30)
            uid = uuid.uuid1()
            print(uid)
            html_message = render_to_string(
                'security/resetPasswordMail.html', context={'user': user, 'token': request.build_absolute_uri('/reset-password/'+str(uid))}, request=request)
            user.email_user(
                subject='Reset Password',
                from_email='Akshara <noreply@akshara.ubiqe.in>',
                message=strip_tags(html_message),
                html_message=html_message,
                fail_silently=True)
            PasswordToken.objects.create(
                User=user, Expiration=expiration, Token=uid)
            return redirect('security:mailed')
    return render(request, 'security/index.html')


def mailed(request):
    return render(request, 'security/mailed.html')


def reset(request, token):
    try:
        user = User.objects.get(ResetToken__Token=token)
    except:
        return redirect('accounts:login')
    if user.ResetToken.Expiration < datetime.datetime.now(datetime.timezone.utc):
        user.ResetToken.delete()
        messages.error(
            request, 'Your link has expired, please put up a new request to change password')
        return redirect('accounts:login')
    if request.method == 'POST':
        user.set_password(request.POST['password'])
        user.save()
        user.ResetToken.delete()
        messages.success(
            request, 'Your password has been reset, you can now login to your account')
        return redirect('accounts:login')
    return render(request, 'security/resetPasswordForm.html', {'token': token})
