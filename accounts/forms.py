from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm,PasswordChangeForm
from .models import *
from django import forms
from student.models import *
from django.contrib.auth import authenticate

class LoginForm(AuthenticationForm):
    class Meta:
        fields = ('Login_id', 'password')
    
class CustomUserForm(UserCreationForm): 
    class Meta:
        model = CustomUser
        fields = ['Login_id', 'first_name', 'last_name','email', 'dob', 'gender', 'phone_number', 'address','password1','password2']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['Login_id', 'first_name','email', 'last_name', 'dob', 'gender', 'phone_number', 'address']