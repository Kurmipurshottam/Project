from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title','date', 'start_time', 'end_time', 'description')

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name','description','start_date','end_date')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_type', 'date', 'start_time', 'end_time', 'standard')

@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'due_date','paid_date','status')

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('teacher','amount','paid_date', 'status')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title','date','description')

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student', 'start_date', 'end_date', 'status')

