from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import User, Class, Student
from lessons.models import Lesson, Subject
from django import http
from django.db.models import Q
import json
from datetime import datetime, timedelta


def deleteChapters(request):
    if request.user.is_authenticated and request.user.admin:
        Lesson.objects.filter(id__in=request.POST.getlist('data[]')).delete()
        data = {
            'message': 'Chapters deleted successfully'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def chapterDetail(request):
    if request.user.is_authenticated and request.user.admin:
        lesson = Lesson.objects.values(
            'id', 'Name', 'Number').get(id=request.GET['id'])
        data = lesson
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def updateChapterDetails(request):
    if request.user.is_authenticated and request.user.admin:
        lesson = Lesson.objects.get(id=request.POST['id'])
        lesson.Name = request.POST['Name']
        lesson.Number = request.POST['Number']
        lesson.save()
        data = {
            'message': 'Details updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': 'Not authorized'})


def uploadStudents(request):
    if request.user.is_authenticated and request.user.admin:
        for x in json.loads(request.POST['file']):
            cla = Class.objects.get(name=x['Class'])
            ordinal = x['dob']
            epoch = datetime(1900, 1, 1)
            if ordinal > 59:
                ordinal -= 1  # Excel leap year bug, 1900 is not a leap year!
            inDays = int(ordinal)
            frac = ordinal - inDays
            inSecs = int(round(frac * 86400.0))
            user = User.objects.create_user(
                email=x['email'],
                password=x['email'],
                first_name=x['First Name'],
                last_name=x['Last Name'],
                user_type='Student'
            )
            Student.objects.create(
                user=user,
                gender=x['gender'],
                Contact=x['Contact'],
                dob=(epoch + timedelta(days=inDays - 1, seconds=inSecs)).date(),
                Address=x['Address'],
                City=x['City'],
                District=x['District'],
                State=x['State'],
                Pincode=x['Pincode'],
                Class=cla
            )
        data = {
            'message': 'File uploaded'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def assignTeacher(request):
    if request.user.is_authenticated and request.user.admin:
        if request.POST['type'] == 'backup':
            Subject.objects.filter(id=request.POST['id']).update(
                backup_teacher=User.objects.get(id=request.POST['teacher']))
        else:
            Subject.objects.filter(id=request.POST['id']).update(
                teacher=User.objects.get(id=request.POST['teacher']))
        data = {
            'message': "Teacher Assigned"
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def editSubject(request):
    if request.user.is_authenticated and request.user.admin:
        Subject.objects.filter(id=request.POST['id']).update(
            Name=request.POST['name'])
        data = {
            'message': "Subject updated"
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def newSubject(request):
    if request.user.is_authenticated and request.user.admin:
        Subject.objects.create(
            Name=request.POST['Name'], Class=Class.objects.get(id=request.POST['id']))
        data = {
            'message': "Subject created"
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def deleteSubject(request):
    if request.user.is_authenticated and request.user.admin:
        Subject.objects.filter(id=request.POST['id']).delete()
        data = {
            'message': "Subject deleted"
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def getSubjects(request):
    if request.user.is_authenticated and request.user.admin:
        subs = Subject.objects.filter(Name__contains=request.GET['term'])
        data = {
            'subject': [{
                'id': s.id,
                'Name': s.Name,
                'Class': s.Class.name,
            } for s in subs]
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def editClass(request):
    if request.user.is_authenticated and request.user.admin:
        Class.objects.filter(id=request.POST['id']).update(
            name=request.POST['name'])
        data = {
            'message': 'Class updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def getClasses(request):
    if request.user.is_authenticated and request.user.admin:
        Classes = Class.objects.filter(
            name__contains=request.GET['term']).values('id', 'name')
        data = {
            'class': list(Classes),
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def deleteClass(request):
    if request.user.is_authenticated and request.user.admin:
        Class.objects.filter(id=request.POST['id']).delete()
        data = {
            'message': 'Class deleted'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def newClass(request):
    if request.user.is_authenticated and request.user.admin:
        Class.objects.create(
            name=request.POST['name'])
        data = {
            'message': 'Class addded'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def newLesson(request):
    if request.user.is_authenticated and request.user.admin:
        lesson = Lesson.objects.create(
            Name=request.POST['lesson'], Number=request.POST['number'], Subject=Subject.objects.get(id=request.POST['id']))
        data = {
            'message': 'Lesson addded'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def updateStaff(request):
    if request.user.is_authenticated and request.user.admin:
        user = User.objects.get(id=request.POST['id'])
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        data = {
            'message': 'Selected User is updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def deleteStaff(request):
    if request.user.is_authenticated and request.user.admin:
        User.objects.filter(id__in=request.POST.getlist('id[]')).delete()
        data = {
            'message': 'Selected Users are deleted'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def getUser(request):
    if request.user.is_authenticated and request.user.admin:
        user = User.objects.get(id=request.GET['id'])
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def newStaff(request):
    if request.user.is_authenticated and request.user.admin:
        # if request.POST['type'] == 'admin':
        #     user = User.objects.create_admin(
        #         email=request.POST['email'],
        #         password=request.POST['email'],
        #         first_name=request.POST['first_name'],
        #         last_name=request.POST['last_name'],
        #         user_type='Staff'
        #     )
        # else:
        user = User.objects.create_staff(
            email=request.POST['email'],
            password=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            user_type='Staff'
        )
        data = {
            'message': 'User added'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def getStaff(request):
    if request.user.is_authenticated and request.user.admin:
        if request.GET['type'] == 'teacher':
            staff = User.objects.filter(is_staff=True)
        elif request.GET['type'] == 'admin':
            staff = User.objects.filter(admin=True)
        else:
            staff = User.objects.filter(Q(admin=True) | Q(is_staff=True))
        staff = staff.filter(Q(first_name__contains=request.GET['term']) | Q(
            last_name__contains=request.GET['term']))
        data = {
            'staff': [{
                'id': x.id,
                'Name': x.get_full_name(),
                'Email': x.email,
            }for x in staff]
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def newStudent(request):
    if request.user.is_authenticated and request.user.admin:
        user = User.objects.create_user(
            email=request.POST['email'],
            password=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            user_type='Student'
        )
        stuent = Student.objects.create(
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
        data = {
            'message': 'User Added'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def getStudent(request):
    if request.user.is_authenticated and request.user.admin:
        user = User.objects.get(id=request.GET['id'])
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.Student.gender,
            'email': user.email,
            'Address': user.Student.Address,
            'City': user.Student.City,
            'District': user.Student.District,
            'dob': user.Student.dob,
            'State': user.Student.State,
            'Pincode': user.Student.Pincode,
            'Contact': user.Student.Contact,
            'Class': user.Student.Class.id,
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def getStudents(request):
    if request.user.is_authenticated and request.user.admin:
        if request.GET['class'] == '':
            Classes = Class.objects.all()
        else:
            Classes = Class.objects.filter(id=request.GET['class'])
        students = Student.objects.filter(Q(user__first_name__contains=request.GET['term']) | Q(
            user__last_name__contains=request.GET['term']), Class__in=Classes)
        data = {
            'students': [{
                'id': stu.user.id,
                'Name': stu.user.get_full_name(),
                'Email': stu.user.email,
                'Contact': stu.Contact,
                'Gender': stu.get_gender_display(),
                'DOB': stu.dob,
                'City': stu.City,
                'State': stu.State,
                'District': stu.District,
                'Pincode': stu.Pincode,
                'Address': stu.Address,
            } for stu in students]
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def updateStudent(request):
    if request.user.is_authenticated and request.user.admin:
        user = User.objects.get(id=request.POST['id'])
        student = user.Student
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        student.gender = request.POST['gender']
        student.Contact = request.POST['Contact']
        student.Address = request.POST['Address']
        student.City = request.POST['City']
        student.District = request.POST['District']
        student.State = request.POST['State']
        student.Pincode = request.POST['Pincode']
        student.Class = Class.objects.get(id=request.POST['Class'])
        student.save()
        data = {
            'message': 'Selected User is updated'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})


def deleteStudents(request):
    if request.user.is_authenticated and request.user.admin:
        User.objects.filter(id__in=request.POST.getlist('id[]')).delete()
        data = {
            'message': 'Selected Users are deleted'
        }
        return http.JsonResponse(data)
    return http.HttpResponseForbidden({'message': "You're not authorized"})
