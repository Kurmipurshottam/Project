from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.contrib.auth import authenticate
from .managers import CustomUserManager

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class CustomUser(AbstractUser):
    Teacher = "Teacher"
    Student = "Student"
    Admin = "Admin"
    USER_TYPE = ((Admin, "Admin"), (Teacher, "Teacher"), (Student, "Student"))
    GENDER = [("Male", "Male"), ("Female", "Female")]

    username = None
    Login_id = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(choices=USER_TYPE, max_length=15,default=Admin)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    phone_number = models.CharField(max_length=11)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profile/',default="default.png")
    USERNAME_FIELD = "Login_id"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()   

    def __str__(self):  
        return f"{self.Login_id}"       
    
    