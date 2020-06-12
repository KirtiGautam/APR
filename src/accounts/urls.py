from django.urls import path
from accounts.views import student_information, log, index, logo, school_staff
from accounts.admin_settings import getStudents, deleteStudents, getStudent, updateStudent, newStudent

app_name = 'accounts'

urlpatterns = [
    #Views
    path('', index, name='dashboard'),
    path('login', log, name='login'),
    path('logout', logo, name='logout'),
    path('settings/student-information',
         student_information, name='student_information'),
    path('settings/school-staff', school_staff, name='staff'),
    #Requests         
    path('get-students', getStudents, name='get-students'),
    path('get-student', getStudent, name='get-student'),
    path('delete-students', deleteStudents, name='delete-students'),
    path('update-student', updateStudent, name='update-student'),
    path('new-student', newStudent, name='new-student'),
]
