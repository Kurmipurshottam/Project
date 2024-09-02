from django.db import models
from django.utils import timezone
from accounts.models import *
from student.models import *

# Create your models here.

class Teacher(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joining_date = models.DateField(default=timezone.now)
    qualification = models.CharField(max_length=100)

    def has_usable_password(self):
        return False

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)
    
class Attendance(BaseModel):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.student.user.first_name