from django.shortcuts import render, redirect
from django import http
from django.contrib.auth import update_session_auth_hash


def changePassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            if not user.check_password(request.POST['pre']):
                data = {
                    'message': 'Old Password is incorrect'
                }
            else:
                user.set_password(request.POST['password'])
                user.save()
                update_session_auth_hash(request, user)
                data = {
                    'message': 'Password Changed successfully'
                }
            return http.JsonResponse(data)
        else:
            return render(request, 'settings/user/passwordChange.html')
    return http.HttpResponseForbidden({'message': 'Not authorized'})
