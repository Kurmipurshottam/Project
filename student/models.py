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

class Demo(models.Model):
    text = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    url = models.URLField()
    tel = models.CharField(max_length=15)
    number = models.IntegerField()
    range = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    datetime = models.DateTimeField()
    month = models.CharField(max_length=7)  # e.g. "2025-04"
    week = models.CharField(max_length=8)   # e.g. "2025-W15"
    checkbox1 = models.BooleanField(default=False)
    checkbox2 = models.BooleanField(default=False)
    radio = models.CharField(max_length=10, choices=[("1", "Radio 1"), ("2", "Radio 2")])
    file = models.FileField(upload_to='uploads/')
    select = models.CharField(max_length=20, choices=[("option1", "Option 1"), ("option2", "Option 2")])
    textarea = models.TextField()
    hidden = models.CharField(max_length=100, default="secret")

    def __str__(self):
        return self.text

from django.db import models

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('cheque', 'Cheque'),
    ]

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)  # New field to identify method
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_intent_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Only for card
    customer_id = models.CharField(max_length=255, null=True, blank=True)  # Optional: Stripe customer ID
    last_4_digits = models.CharField(max_length=4, null=True, blank=True)  # Only for card
    card_type = models.CharField(max_length=50, null=True, blank=True)  # Visa, MasterCard, etc.
    expiration_date = models.CharField(max_length=7, null=True, blank=True)  # MM/YY format
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Only for card

    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.payment_method.capitalize()} Payment - {self.payment_status}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

