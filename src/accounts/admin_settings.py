from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import User, Class, Student
from django import http
from django.db.models import Q


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

