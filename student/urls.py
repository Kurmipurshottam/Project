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
from . import views
from student.views  import *

app_name = 'Student'

urlpatterns = [
    path('studentdashboard', StudentDashboard.as_view(), name='studentdashboard'),
    path('leavelist', LeaveList.as_view(), name='leavelist'),
    path('leave/add/', AddLeave.as_view(), name='addleave'),
    path('leave/delete/<int:pk>/', DeleteLeave.as_view(), name='deleteleave'),
    path('leave/edit/<int:pk>/', EditLeave.as_view(), name='editleave'),
    path('demo/', Demoview.as_view(), name='demo'),
    path("create-payment-intent/", CreatePaymentIntentView.as_view(), name="create_payment_intent"),
     path('save_payment/', views.save_payment, name='save_payment'),
]