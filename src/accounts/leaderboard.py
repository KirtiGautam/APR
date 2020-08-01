from django.shortcuts import render, redirect
from django import http
from accounts.models import (Student, Class)
import math
from lessons.models import (
    user_progress_pdf as lesson_video_progress,
    user_progress_video as lesson_pdf_progress,
    Comment,
    lesson_video_likes,
    Video as lesson_vid,
    Pdf as lesson_pd,
)
from assignments.models import (
    user_progress_pdf as assignment_video_progress,
    user_progress_video as assignment_pdf_progress,
    AComment,
    assignment_video_likes,
    Video as assignment_vid,
    Pdf as assignment_pd,
)
from homework.models import (
    user_progress_pdf as homework_video_progress,
    user_progress_video as homework_pdf_progress,
    HComment,
    homework_video_likes,
    Video as homework_vid,
    Pdf as homework_pd,
)
import datetime
from django.utils import timezone


def leaderboard(request):
    if request.user.is_authenticated and (request.user.user_type == 'Student' or request.user.admin):
        if request.GET['time'] == 'weekly':
            constraint = datetime.datetime.now(
                datetime.timezone.utc)-datetime.timedelta(days=6)
        elif request.GET['time'] == 'monthly':
            constraint = datetime.datetime.now(
                datetime.timezone.utc) - datetime.timedelta(days=30)
        else:
            constraint = timezone.make_aware(datetime.datetime.combine(
                datetime.date(1999, 11, 25), datetime.datetime.min.time()))
        data = []
        # Get All Students of same class
        if request.user.user_type == 'Student':
            this_class = request.user.Student.Class
            students = Student.objects.filter(
                Class=this_class, user__status="A")
        if request.user.admin:
            if 'Class' in request.GET:
                this_class = Class.objects.get(id=request.GET['Class'])
                students = Student.objects.filter(
                    Class=this_class, user__status="A")
            else:
                this_class = Class.objects.all().first()
                students = Student.objects.filter(
                    Class=this_class, user__status="A")

        # Progress Section
        total_lesson_video_count = lesson_vid.objects.filter(
            lesson__Subject__Class=this_class, created__gte=constraint)  # All lesson videos count

        total_lesson_pdf_count = lesson_pd.objects.filter(
            lesson__Subject__Class=this_class, created__gte=constraint)  # All lesson pdfs count

        total_assignment_video_count = assignment_vid.objects.filter(
            lesson__Subject__Class=this_class, created__gte=constraint)  # All assignment videos count

        total_assignment_pdf_count = assignment_pd.objects.filter(
            lesson__Subject__Class=this_class, created__gte=constraint)  # All assignment pdfs count

        total_homework_video_count = homework_vid.objects.filter(
            lesson__Subject__Class=this_class, created__gte=constraint)  # All homework videos count

        total_homework_pdf_count = homework_pd.objects.filter(
            lesson__Subject__Class=this_class, created__gte=constraint)  # All homework  pdfs count

        # Comments Section
        total_lesson_Comments = Comment.objects.filter(
            Video__in=total_lesson_video_count, Author__user_type='Student', created__gte=constraint)
        total_assignment_Comments = AComment.objects.filter(
            Video__in=total_assignment_video_count, Author__user_type='Student', created__gte=constraint)
        total_homework_Comments = HComment.objects.filter(
            Video__in=total_homework_video_count, Author__user_type='Student', created__gte=constraint)

        # Likes Section
        total_lesson_likes = lesson_video_likes.objects.filter(
            Comment__in=total_lesson_Comments, User__user_type='Student')
        total_assignment_likes = assignment_video_likes.objects.filter(
            AComment__in=total_assignment_Comments, User__user_type='Student')
        total_homework_likes = homework_video_likes.objects.filter(
            HComment__in=total_homework_Comments, User__user_type='Student')

        # Appreciate Section
        total_lesson_appreciates = lesson_video_likes.objects.filter(
            Comment__in=total_lesson_Comments, User__user_type='Staff')
        total_assignment_appreciates = assignment_video_likes.objects.filter(
            AComment__in=total_assignment_Comments, User__user_type='Staff')
        total_homework_appreciates = homework_video_likes.objects.filter(
            HComment__in=total_homework_Comments, User__user_type='Safft')

        mydata = None
        maxdata = None

        for x in students:
            # Category 4
            student_watched_lesson_video = x.user.watched_lesson_video.filter(
                Video__in=total_lesson_video_count)  # Get lesson watched videos

            student_read_lesson_pdf = x.user.read_lesson_pdf.filter(
                Pdf__in=total_lesson_pdf_count)  # Get lesson read pdfs

            student_watched_homework_video = x.user.watched_homework_video.filter(
                Video__in=total_homework_video_count)  # Get homework watched videos

            student_read_homework_pdf = x.user.read_homework_pdf.filter(
                Pdf__in=total_homework_pdf_count)  # Get homework read pdfs

            student_watched_assignment_video = x.user.watched_assignment_video.filter(
                Video__in=total_assignment_video_count)  # Get assignment watched videos

            student_read_assignment_pdf = x.user.read_assignment_pdf.filter(
                Pdf__in=total_assignment_pdf_count)  # Get assignment read pdfs

            if sum([total_lesson_video_count.count(), total_homework_video_count.count(), total_assignment_video_count.count(), total_assignment_pdf_count.count(), total_homework_pdf_count.count(), total_lesson_pdf_count.count()]) > 0:
                category4 = math.floor((sum([student_watched_lesson_video.count(), student_watched_assignment_video.count(), student_watched_homework_video.count(), student_read_homework_pdf.count(), student_read_assignment_pdf.count(), student_read_lesson_pdf.count()]) /
                                        sum([total_lesson_video_count.count(), total_homework_video_count.count(), total_assignment_video_count.count(), total_assignment_pdf_count.count(), total_homework_pdf_count.count(), total_lesson_pdf_count.count()]))*100)
            else:
                category4 = 0

            # Category 1
            student_lesson_comments = total_lesson_Comments.filter(
                Author__id=x.user.id)  # Get Student lesson Comment

            student_assignment_comments = total_assignment_Comments.filter(
                Author__id=x.user.id)  # Get Student Assignment Comment

            student_homework_comments = total_homework_Comments.filter(
                Author__id=x.user.id)  # Get Student Homework Comment

            if sum([total_lesson_Comments.count(), total_assignment_Comments.count(), total_homework_Comments.count()]) > 0:
                category1 = sum([student_lesson_comments.count(
                ), student_homework_comments.count(), student_assignment_comments.count()])
            else:
                category1 = 0

            # Category 2
            student_lesson_likes = total_lesson_likes.filter(
                Comment__Author__id=x.user.id)  # Get Student Lesson likes

            student_assignment_likes = total_assignment_likes.filter(
                AComment__Author__id=x.user.id)  # Get Student assignment likes

            student_homework_likes = total_homework_likes.filter(
                HComment__Author__id=x.user.id)  # Get Student homework likes

            if sum([total_lesson_likes.count(), total_assignment_likes.count(), total_homework_likes.count()]) > 0:
                category2 = sum([student_lesson_likes.count(
                ), student_homework_likes.count(), student_assignment_likes.count()])
            else:
                category2 = 0

            # Category 3
            student_lesson_appreciates = total_lesson_appreciates.filter(
                Comment__Author__id=x.user.id)  # Get Student Lesson appreciates

            student_assignment_appreciates = total_assignment_appreciates.filter(
                AComment__Author__id=x.user.id)  # Get Student assignment appreciates
            student_homework_appreciates = total_homework_appreciates.filter(
                HComment__Author__id=x.user.id)  # Get Student homework appreciates

            if sum([total_lesson_appreciates.count(), total_assignment_appreciates.count(), total_homework_appreciates.count()]) > 0:
                category3 = sum([student_lesson_appreciates.count(
                ), student_homework_appreciates.count(), student_assignment_appreciates.count()])
            else:
                category3 = 0

            final_points = round((category1+(category2*3) +
                                  (category3*5))*(0.5+(category4/100)), 1)

            if request.user == x.user:
                mydata = {
                    'category_1': category1,
                    'category_2': category2,
                    'category_3': category3,
                    'category_4': category4,
                    'finalpoints': final_points,
                }
            if maxdata is None:
                maxdata = {
                    'category_1': category1,
                    'category_2': category2,
                    'category_3': category3,
                    'category_4': category4,
                }
            else:
                if maxdata['category_1'] < category1:
                    maxdata['category_1'] = category1
                if maxdata['category_2'] < category2:
                    maxdata['category_2'] = category2
                if maxdata['category_3'] < category3:
                    maxdata['category_3'] = category3
                if maxdata['category_4'] < category4:
                    maxdata['category_4'] = category4

            data.append({
                'Student': x,
                'category_1': category1,
                'category_2': category2,
                'category_3': category3,
                'category_4': category4,
                'finalpoints': final_points,
            })

        data = {
            'data': sorted(data, key=lambda i: i['finalpoints'], reverse=True),
            'mydata': mydata,
            'maxdata': maxdata,
        }
        if request.user.admin:
            data['Classes'] = Class.objects.all()
            data['class_select'] = Class.objects.first(
            ).id if 'Class' not in request.GET else request.GET['Class']
        return render(request, 'leaderboard/leaderboard.html', data)
    return redirect('accounts:login')
