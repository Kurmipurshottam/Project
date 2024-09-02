from .models import *
from django import forms
from django.core.exceptions import ValidationError
import datetime

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','date', 'start_time', 'end_time','description']

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['name','description','start_date','end_date']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['date', 'start_time', 'end_time', 'standard', 'exam_type']

class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = ['student', 'amount', 'due_date', 'paid_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'paid_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_paid_date(self):
        paid_date = self.cleaned_data.get('paid_date')
        due_date = self.cleaned_data.get('due_date')

        if paid_date and due_date and paid_date >= due_date:
            raise ValidationError("Paid date cannot be on or after the due date.")
        
        return paid_date

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['teacher', 'amount', 'paid_date', 'status']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title','description']

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'reason']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Remove the teacher and student fields from the form
        self.fields.pop('teacher', None)
        self.fields.pop('student', None)