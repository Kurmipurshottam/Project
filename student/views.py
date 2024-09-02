from django.shortcuts import render,redirect
from django.views.generic import *
from custom_admin.models import *
from django.urls import reverse_lazy
from custom_admin.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class StudentDashboard(TemplateView):
    template_name = "Student/student-dashboard.html"

#  **************************************************************
#  ************************* Leaves *****************************
#  **************************************************************

class LeaveList(LoginRequiredMixin, ListView):
    model = Leave
    template_name = 'Student/student-leave.html'
    context_object_name = 'leaves'
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == CustomUser.Teacher:
            try:
                teacher_instance = Teacher.objects.get(user=user)
                return Leave.objects.filter(teacher=teacher_instance)
            except Teacher.DoesNotExist:
                return Leave.objects.none()  # Handle case where Teacher instance is not found
        
        elif user.user_type == CustomUser.Student:
            try:
                student_instance = Student.objects.get(user=user)
                return Leave.objects.filter(student=student_instance)
            except Student.DoesNotExist:
                return Leave.objects.none()  # Handle case where Student instance is not found
        
        else:
            return Leave.objects.none()  # Return empty queryset for other user types

class AddLeave(CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'Student/student-add-leave.html'
    success_url = reverse_lazy('Student:leavelist') 

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = self.request.user
        
        if form.is_valid():
            if user.user_type == CustomUser.Student:
                try:
                    student_instance = Student.objects.get(user=user)
                    form.instance.student = student_instance
                except Student.DoesNotExist:
                    return self.form_invalid(form)  # Handle error if Student instance not found
                
            elif user.user_type == CustomUser.Teacher:
                try:
                    teacher_instance = Teacher.objects.get(user=user)
                    form.instance.teacher = teacher_instance
                except Teacher.DoesNotExist:
                    return self.form_invalid(form)  # Handle error if Teacher instance not found
            
            # Save the form instance and redirect
            return self.form_valid(form)
        
        return self.form_invalid(form)
        

class DeleteLeave(LoginRequiredMixin,DeleteView):     
    model =  Leave
    template_name = 'Student/student-leave.html'
    success_url = reverse_lazy('Student:leavelist')   

class EditLeave(LoginRequiredMixin,UpdateView): 
    template_name = 'Student/student-edit-leave.html'
    model = Leave
    form_class = LeaveForm
    success_url = reverse_lazy('Student:leavelist')    