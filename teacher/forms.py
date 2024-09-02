from .models import *
from django import forms

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['joining_date', 'qualification']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']