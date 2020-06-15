from django.urls import path
from accounts.views import (
    student_information,
    log,
    index,
    logo,
    school_staff,
    classes,
    chapters
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
    updateStaff,
    newLesson,
    newClass,
    deleteClass,
    getClasses,
    editClass,
    getSubjects,
    deleteSubject,
    newSubject,
    editSubject,
    assignTeacher
)

app_name = 'accounts'

urlpatterns = [
    # Views
    path('', index, name='dashboard'),
    path('login', log, name='login'),
    path('logout', logo, name='logout'),
    path('settings/chapters', chapters, name='chapters'),
    path('settings/classes', classes, name='classes'),
    path('settings/student-information',
         student_information, name='student_information'),
    path('settings/school-staff', school_staff, name='staff'),
    # Requests
    path('assign-teacher', assignTeacher, name='assign-teacher'),
    path('edit-subject', editSubject, name='edit-subject'),
    path('new-subject', newSubject, name='new-subject'),
    path('delete-subject', deleteSubject, name='delete-subject'),
    path('get-subs', getSubjects, name='get-subs'),
    path('edit-class', editClass, name='edit-class'),
    path('get-class', getClasses, name='get-class'),
    path('delete-class', deleteClass, name='delete-class'),
    path('new-class', newClass, name='new-class'),
    path('new-lesson', newLesson, name='new-lesson'),
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
