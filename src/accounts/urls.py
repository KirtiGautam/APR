from django.urls import path
from accounts.views import (
    student_information,
    log,
    index,
    logo,
    school_staff
)
from accounts.admin_settings import (
    getStudents,
    deleteStudents,
    getStudent,
    updateStudent,
    newStudent,
    getStaff,
    getUser,
    newStaff,
    deleteStaff,
    updateStaff
)

app_name = 'accounts'

urlpatterns = [
    # Views
    path('', index, name='dashboard'),
    path('login', log, name='login'),
    path('logout', logo, name='logout'),
    path('settings/student-information',
         student_information, name='student_information'),
    path('settings/school-staff', school_staff, name='staff'),
    # Requests
    path('get-staff', getStaff, name='get-staff'),
    path('get-user', getUser, name='get-user'),
    path('delete-staff', deleteStaff, name='delete-staff'),
    path('update-staff', updateStaff, name='update-staff'),
    path('new-staff', newStaff, name='new-staff'),
    path('get-students', getStudents, name='get-students'),
    path('get-student', getStudent, name='get-student'),
    path('delete-students', deleteStudents, name='delete-students'),
    path('update-student', updateStudent, name='update-student'),
    path('new-student', newStudent, name='new-student'),
]
