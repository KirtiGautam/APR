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


def leaderboard(request):
    if request.user.is_authenticated:
        from lessons.models import (
            user_progress_pdf as lesson_video_progress,
            user_progress_video as lesson_pdf_progress,
            Comment
        )
        from homework.models import (
            user_progress_pdf as homework_video_progress,
            user_progress_video as homework_pdf_progress,
            HComment
        )
        from assignments.models import (
            user_progress_pdf as assignment_video_progress,
            user_progress_video as assignment_pdf_progress,
            AComment
        )
        likes

        return render(request, 'leaderboard/leaderboard.html')
    return http.HttpResponseForbidden({'message': 'Unauthorized'})
