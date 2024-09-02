from django.db import models
from django.utils import timezone
from accounts.models import *
from teacher.models import *
from django.db.models import Max

class Standard(BaseModel):

    STANDARD_CHOICES = [(i, f'Standard {i}') for i in range(1, 13)]

    standard = models.PositiveIntegerField(choices=STANDARD_CHOICES, default=1)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.standard}"

class Student(BaseModel):
    # STANDARD_CHOICES = [(i, f'Standard {i}') for i in range(1, 13)]  # Example for standards 1 to 12

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    roll_no = models.PositiveIntegerField(blank=True, null=True)  # Automatically assigned
    joining_date = models.DateField(default=timezone.now)
    # standard = models.PositiveIntegerField(choices=STANDARD_CHOICES, default=1)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def has_usable_password(self):
        return False

    def delete(self, *args, **kwargs):
        # Store the current roll number and standard before deleting
        roll_no = self.roll_no
        standard = self.standard
        
        # Delete the student
        self.user.delete()
        super().delete(*args, **kwargs)
        
        # Update roll numbers of other students in the same standard
        students = Student.objects.filter(standard=standard, roll_no__gt=roll_no).order_by('roll_no')
        for student in students:
            student.roll_no -= 1
            student.save()

    def save(self, *args, **kwargs):
        if self.pk:  # If this is an update (existing student)
            old_student = Student.objects.get(pk=self.pk)
            old_standard = old_student.standard
            old_roll_no = old_student.roll_no

            # If the standard has changed
            if self.standard != old_standard:
                # Adjust roll numbers in the old standard
                if old_standard:
                    students_in_old_standard = Student.objects.filter(standard=old_standard, roll_no__gt=old_roll_no).order_by('roll_no')
                    for student in students_in_old_standard:
                        student.roll_no -= 1
                        student.save()

                # Adjust roll numbers in the new standard
                if self.standard:
                    max_roll_no_result = Student.objects.filter(standard=self.standard).aggregate(Max('roll_no'))
                    max_roll_no = max_roll_no_result.get('roll_no__max')
                    if max_roll_no is not None:
                        self.roll_no = max_roll_no + 1
                    else:
                        self.roll_no = 1

                super(Student, self).save(*args, **kwargs)

                # Adjust roll numbers in the new standard for other students
                if self.roll_no:
                    students_in_new_standard = Student.objects.filter(standard=self.standard, roll_no__gt=self.roll_no).order_by('roll_no')
                    for student in students_in_new_standard:
                        student.roll_no += 1
                        student.save()
            else:
                # If the standard hasn't changed, just handle roll number assignment
                if not self.roll_no:
                    max_roll_no_result = Student.objects.filter(standard=self.standard).aggregate(Max('roll_no'))
                    max_roll_no = max_roll_no_result.get('roll_no__max')
                    if max_roll_no is not None:
                        self.roll_no = max_roll_no + 1
                    else:
                        self.roll_no = 1
                super(Student, self).save(*args, **kwargs)
                
        else:  # If this is a new student (creation)
            max_roll_no_result = Student.objects.filter(standard=self.standard).aggregate(Max('roll_no'))
            max_roll_no = max_roll_no_result.get('roll_no__max')
            if max_roll_no is not None:
                self.roll_no = max_roll_no + 1
            else:
                self.roll_no = 1

            super(Student, self).save(*args, **kwargs)

    

