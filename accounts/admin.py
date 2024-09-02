from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('Login_id','first_name','last_name','dob','email','gender','phone_number','user_type','address')
