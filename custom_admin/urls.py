"""
URL configuration for sms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from student.views  import *
from accounts.views  import *
from .views  import *

app_name = 'Admin'

urlpatterns = [
    path('admindashboard/', AdminDashboard.as_view(), name='admindashboard'),
    #  students urls
    path('student/', StudentList.as_view(), name='studentlist'),
    path('student/add/', AddStudent.as_view(), name='addstudent'),
    path('student/delete/<int:pk>/', DeleteStudent.as_view(), name='deletestudent'),
    path('student/edit/<int:pk>/', EditStudent.as_view(), name='editstudent'),
    # teachers Urls
    path('teacher/', TeacherList.as_view(), name='teacherlist'),
    path('teacher/add/', AddTeacher.as_view(), name='addteacher'),
    path('teacher/delete/<int:pk>/', DeleteTeacher.as_view(), name='deleteteacher'),
    path('teacher/edit/<int:pk>/', EditTeacher.as_view(), name='editteacher'),
    # event urls
    path('event/', EventList.as_view(), name='eventlist'),
    path('event/add/', AddEvent.as_view(), name='addevent'),
    path('event/delete/<int:pk>/', DeleteEvent.as_view(), name='deleteevent'),
    path('event/edit/<int:pk>/', EditEvent.as_view(), name='editevent'),
    # holiday urls
    path('holiday/', HolidayList.as_view(), name='holidaylist'),
    path('holiday/add/', AddHoliday.as_view(), name='addholiday'),
    path('holiday/delete/<int:pk>/', DeleteHoliday.as_view(), name='deleteholiday'),
    path('holiday/edit/<int:pk>/', EditHoliday.as_view(), name='editholiday'),
    #Attendence urls
    path('attendence/', AttendenceList.as_view(), name='attendencelist'),
    #Exam urls
    path('exam/', ExamList.as_view(), name='examlist'),
    path('exam/add/', AddExam.as_view(), name='addexam'),
    path('exam/delete/<int:pk>/', DeleteExam.as_view(), name='deleteexam'),
    path('exam/edit/<int:pk>/', EditExam.as_view(), name='editexam'),
    #Fees urls
    path('fees/',FeesList.as_view(), name='feeslist'),
    path('fees/add/', AddFees.as_view(), name='addfees'),
    path('fees/delete/<int:pk>/', DeleteFees.as_view(), name='deletefees'),
    path('fees/edit/<int:pk>/', EditFees.as_view(), name='editfees'),
    #Salary urls
    path('salary/',SalaryList.as_view(), name='salarylist'),
    path('salary/add/', AddSalary.as_view(), name='addsalary'),
    path('salary/delete/<int:pk>/', DeleteSalary.as_view(), name='deletesalary'),
    path('salary/edit/<int:pk>/', EditSalary.as_view(), name='editsalary'),
    #Notice urls
    path('notice/',NoticeList.as_view(), name='noticelist'),
    path('notice/add/', AddNotice.as_view(), name='addnotice'),
    path('notice/delete/<int:pk>/', DeleteNotice.as_view(), name='deletenotice'),
    path('notice/edit/<int:pk>/', EditNotice.as_view(), name='editnotice'),
]