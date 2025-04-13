from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','joining_date','roll_no','standard')

@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'standard')

admin.site.register(Demo)
admin.site.register(Payment)