from django.shortcuts import render, redirect
from django import http
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib import messages
from .models import (Post, Likes, Comment)


def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post.objects.create(
                Body=request.POST['body'], Owner=request.user)
            if request.POST['category'] != 'null':
                post.Tag = request.POST['category']
                post.save()
            if 'photo' in request.FILES:
                post.Picture = request.FILES['photo']
                post.save()
            return http.JsonResponse(render_to_string('posts/post.html', {'posts': [post]}, request=request), safe=False)
        offset = int(request.GET['offset'])
        if 'type' in request.GET and request.GET['type'] == 'M':
            posts = Post.objects.filter(Owner=request.user)
        elif request.user.admin:
            posts = Post.objects.all()
        elif request.user.is_staff:
            posts = Post.objects.filter(Q(Owner__admin=True) | Q(Owner__is_staff=True) | Q(
                Owner__Student__Class__Subject__in=request.user.teacher.all()))
        else:
            posts = Post.objects.filter(Q(Owner__admin=True) | Q(
                Owner__teacher__in=request.user.Student.Class.Subject.all()) | Q(Owner__Student__Class=request.user.Student.Class))
        if 'type' in request.GET and request.GET['type'] != 'M':
            posts = posts.filter(Tag=request.GET['type'])
        if not posts[offset*10:offset*10+10].exists():
            return http.JsonResponse({'all': True})
        return http.JsonResponse(render_to_string('posts/post.html', {'posts': posts.order_by('-Created')[offset*10:offset*10+10]}, request=request), safe=False)
    return http.HttpResponseForbidden("Not Allowed")


def likePost(request):
    if request.user.is_authenticated and request.method == 'POST':
        post = Post.objects.get(id=request.POST['id'])
        liked = False
        if post.Likes.filter(id=request.user.id).exists():
            post.Likes.remove(request.user)
        else:
            post.Likes.add(request.user)
            liked = True
        post.save()
        data = {
            'count': post.Likes.all().count(),
            "liked": "Post Liked" if liked else 'Post Disliked'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not Allowed")


def likePostComment(request):
    if request.user.is_authenticated and request.method == 'POST':
        comment = Comment.objects.get(id=request.POST['id'])
        liked = False
        if comment.Likes.filter(id=request.user.id).exists():
            comment.Likes.remove(request.user)
        else:
            comment.Likes.add(request.user)
            liked = True
        comment.save()
        data = {
            'count': comment.Likes.all().count(),
            "liked": "Comment Liked" if liked else 'Comment Disliked'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not Allowed")


def single(request, id):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id=id)
        except:
            return http.HttpResponseNotFound('No such Post')
        if request.method == 'POST':
            comment = Comment.objects.create(
                body=request.POST['Comment'], Post=post, Author=request.user)
            if 'hidden_comment_id' in request.POST:
                comment.parent = Comment.objects.get(
                    id=request.POST['hidden_comment_id'])
                comment.save()
            print(request.POST)
            return redirect('posts:post', id=id)
        data = {
            'post': post
        }
        return render(request, 'posts/post-one.html', data)
    return redirect('accounts:login')


def updatePost(request):
    if request.user.is_authenticated and request.method == 'POST':
        post = Post.objects.get(id=request.POST['id'])
        post.Body = request.POST['updated_body']
        post.save()
        return http.JsonResponse("Success", safe=False)
    return redirect('accounts:login')


def deletePost(request, id):
    if request.user.is_authenticated:
        Post.objects.filter(id=id).delete()
        messages.success(request, 'Post Deleted')
        return redirect('accounts:dashboard')
    return redirect('accounts:login')


def analysis(request):
    if request.user.is_authenticated and request.user.user_type == 'Student':
        user = request.user
        from django.db.models import Avg, Max, Sum
        from accounts.models import User
        students = User.objects.filter(
            user_type='Student', Student__Class=user.Student.Class, status="A")

        # Comprehensive skills
        average_posts = Post.objects.filter(
            Owner__in=students).count()/students.count()
        my_posts = user.Post.all().count()
        print(round(average_posts, 2), my_posts)

        # Social skills
        post_coms = Comment.objects.filter(
            Author__in=students).count()/students.count()
        from lessons.models import Comment as LComm, pdfComment
        les_vid_coms = LComm.objects.filter(
            Author__in=students).count()/students.count()
        les_pdf_coms = pdfComment.objects.filter(
            Author__in=students).count()/students.count()
        average_comments = sum([post_coms, les_vid_coms, les_pdf_coms])
        my_comments = sum([user.Post_Comment.all().count(), user.lesson_video_comments.all(
        ).count(), user.lesson_pdf_comments.all().count(), ])
        print(round(average_comments, 2), my_comments)

        # Popularity
        from lessons.models import lesson_pdf_likes, lesson_video_likes
        av_pdf_likes = lesson_pdf_likes.objects.filter(
            pdfComment__Author__in=students).count() / students.count()
        av_vid_likes = lesson_video_likes.objects.filter(
            Comment__Author__in=students).count()/students.count()
        my_likes = lesson_pdf_likes.objects.filter(pdfComment__Author=user).count(
        )+lesson_video_likes.objects.filter(Comment__Author=user).count()
        print(av_vid_likes+av_pdf_likes, my_likes)

        # Lectures Attended
        from lessons.models import user_progress_pdf, user_progress_video
        av_pdf_prog = user_progress_pdf.objects.filter(
            User__in=students).count()/students.count()
        av_vid_prog = user_progress_video.objects.filter(
            User__in=students).count()/students.count()
        my_prog = user.read_lesson_pdf.all().count()+user.watched_lesson_video.all().count()

        data = {
            'popularity': {'mine': my_likes, 'average': round(av_vid_likes+av_pdf_likes, 2)},
            'lectures': {'mine': my_likes, 'average': round(av_vid_prog+av_pdf_prog, 2)},
            'social': {'mine': my_comments, 'average': round(average_comments, 2)},
            'comprehensive': {'mine': my_posts, 'average': round(average_posts, 2)},
        }

        return render(request, 'analysis/index.html', data)
    return redirect('accounts:login')
