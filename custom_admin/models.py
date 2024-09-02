from django.db import models
from django.utils import timezone
from accounts.models import *
from student.models import *
from teacher.models import *
# Create your models here.

class Event(BaseModel):
    title = models.CharField(max_length=30)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return self.title
    
class Holiday(BaseModel):
    name = models.CharField(max_length=30)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Exam(BaseModel):
    EXAM_TYPE_CHOICES = [
        ('Final Exam', 'Final Exam'),
        ('Midterm Exam', 'Midterm Exam'),
    ]
    STANDARD_CHOICES = [(i, f'Standard {i}') for i in range(1, 13)]
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    standard = models.PositiveIntegerField(choices=STANDARD_CHOICES, default=1)
    exam_type = models.CharField(max_length=20,choices=EXAM_TYPE_CHOICES)

    def __str__(self):
        return self.exam_type
    
class Fees(BaseModel):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    def __str__(self):
        return f"{self.student.user.Login_id}"
    
class Salary(BaseModel):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    amount = models.CharField(max_length=25)
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.teacher.user.Login_id}"
    
class Notice(BaseModel):
    title = models.CharField(max_length=25)  
    date = models.DateField(default=timezone.now)
    description = models.TextField()               

    def __str__(self):
        return self.title 

class Leave(BaseModel):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Pending')

    def __str__(self):
        return self.reason

    # def save(self, *args, **kwargs):
    #     # Ensure only one of teacher or student is set
    #     if not (self.teacher or self.student):
    #         raise ValueError("Either teacher or student must be set.")
    #     if self.teacher and self.student:
    #         raise ValueError("Only one of teacher or student should be set.")
    #     super().save(*args, **kwargs)



