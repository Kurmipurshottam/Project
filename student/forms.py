from .models import *
from django import forms

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no','joining_date','standard']

