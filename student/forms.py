from .models import *
from django import forms

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no','joining_date','standard']

from django import forms
import re
from django.core.exceptions import ValidationError

class DemoForm(forms.Form):
    # Text Inputs
    text = forms.CharField(label='Text', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    search = forms.CharField(label='Search', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    url = forms.URLField(label='URL', required=True, widget=forms.URLInput(attrs={'class': 'form-control'}))

    tel = forms.CharField(
        label='Telephone',
        required=True,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Number Inputs
    number = forms.IntegerField(label='Number', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    range = forms.IntegerField(
        label='Range',
        required=True,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'class': 'form-range'})
    )

    # Date/Time Inputs
    date = forms.DateField(
        label='Date',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )
    time = forms.TimeField(
        label='Time',
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        input_formats=['%H:%M']
    )
    datetime = forms.DateTimeField(
        label='Datetime-local',
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    month = forms.DateField(
        label='Month',
        required=True,
        widget=forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
        input_formats=['%Y-%m']
    )
    week = forms.DateField(
        label='Week',
        required=True,
        widget=forms.DateInput(attrs={'type': 'week', 'class': 'form-control'}),
        input_formats=['%Y-W%W']
    )
    zip_code = forms.CharField(
        label='Zip Code',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=10,
    )
    # Checkboxes
    checkbox1 = forms.BooleanField(label='Checkbox 1', required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    checkbox2 = forms.BooleanField(label='Checkbox 2', required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    # Radio Options
    radio = forms.ChoiceField(
        label='Radio Options',
        choices=[(1, 'Radio 1'), (2, 'Radio 2')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )

    # File Upload
    file = forms.FileField(label='File', required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))

    # Select Menu
    select = forms.ChoiceField(
        label='Select an Option',
        choices=[('', 'Choose...'), ('option1', 'Option 1'), ('option2', 'Option 2')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    # Textarea
    textarea = forms.CharField(
        label='Textarea',
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    # Hidden Field
    hidden = forms.CharField(widget=forms.HiddenInput(), initial='secret', required=True)

    # --- Custom Validation ---
    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if not re.match(r'^\d{10}$', tel):
            raise ValidationError("Enter a valid 10-digit mobile number.")
        return tel

    def clean_select(self):
        select = self.cleaned_data.get('select')
        if select == '':
            raise ValidationError("Please choose a valid option.")
        return select

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not re.match(r'^\d{5}(-\d{4})?$', zip_code):  # US-style zip code (XXXXX or XXXXX-XXXX)
            raise ValidationError("Enter a valid zip code (e.g., 12345 or 12345-6789).")
        return zip_code
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'