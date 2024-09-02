from django.urls import reverse
from accounts.forms import *
from student.forms import *
from teacher.forms import *
from .forms import *
from django.views.generic import *
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

# Create your views here.

class AdminDashboard(LoginRequiredMixin,TemplateView):
    template_name = 'Admin/admin-dashboard.html'

#  **************************************************************
#  ************************ Student *****************************
#  **************************************************************

class AddStudent(LoginRequiredMixin,CreateView):
    template_name = 'Admin/admin-add-student.html'
    form_class = CustomUserForm # Main form class   
    student_form_class = StudentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_form'] = self.student_form_class(self.request.POST or None)
        return context

    def form_valid(self, form):
        user_form = form # access the main form object
        student_form = self.student_form_class(self.request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = CustomUser.Student
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            print("===============",student.user.password)
            student.save()  
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form)
        return response
    
    def get_success_url(self):
        return reverse_lazy('Admin:studentlist')  
    
class StudentList(LoginRequiredMixin,ListView):
    model=Student
    template_name = 'Admin/admin-student.html'
    context_object_name = 'students'
    
class DeleteStudent(LoginRequiredMixin,DeleteView):
    model =  Student
    template_name = 'Admin/admin-student.html'
    success_url = reverse_lazy('Admin:studentlist')  

    def Delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class EditStudent(LoginRequiredMixin, UpdateView):
    template_name = 'Admin/admin-edit-student.html'
    form_class = CustomUserChangeForm
    student_form_class = StudentForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk is None:
            raise Http404("Primary key not provided")
        student = get_object_or_404(Student, pk=pk)
        return student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        user = student.user
        user_form = self.form_class(instance=user)
        student_form = self.student_form_class(instance=student)
        context['user_form'] = user_form
        context['student_form'] = student_form
        return context

    def form_valid(self, form):
        # First, handle the CustomUserChangeForm
        response = super().form_valid(form)
        user = self.get_object().user
        student = self.get_object()
        
        # Process and save the StudentForm
        student_form = self.student_form_class(self.request.POST, instance=student)
        user_form = self.form_class(self.request.POST, instance=user)
        if student_form.is_valid() and user_form.is_valid():
            user_form.save()
            student_form.save()
            print("Student form saved.")
        else:
            print("Student form errors:", student_form.errors)
        return response

    def form_invalid(self, form):
        print("Form invalid.")
        student = self.get_object()
        student_form = self.student_form_class(self.request.POST, instance=student)
        return self.render_to_response(self.get_context_data(form=form, student_form=student_form))

    def get_success_url(self):
        return reverse('Admin:studentlist') 

#  **************************************************************
#  ************************ Teacher *****************************
#  **************************************************************
#   
class AddTeacher(LoginRequiredMixin,CreateView):
    template_name = 'Admin/admin-add-teacher.html'
    form_class = CustomUserForm # Main form class   
    teacher_form_class = TeacherForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_form'] = self.teacher_form_class(self.request.POST or None)
        return context

    def form_valid(self, form):
        user_form = form # access the main form object
        teacher_form = self.teacher_form_class(self.request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = CustomUser.Teacher
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()  
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form)
        return response
    
    def get_success_url(self):
        return reverse_lazy('Admin:teacherlist')      

class TeacherList(LoginRequiredMixin,ListView):
    model=Teacher
    template_name = 'Admin/admin-teacher.html'
    context_object_name = 'teachers'  

class DeleteTeacher(LoginRequiredMixin,DeleteView):
    model =  Teacher
    template_name = 'Admin/admin-teacher.html'
    success_url = reverse_lazy('Admin:teacherlist')  

    def Delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)          

class EditTeacher(LoginRequiredMixin, UpdateView):
    template_name = 'Admin/admin-edit-teacher.html'
    form_class = CustomUserChangeForm
    teacher_form_class = TeacherForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk is None:
            raise Http404("Primary key not provided")
        teacher = get_object_or_404(Teacher, pk=pk)
        return teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.get_object()
        user = teacher.user
        user_form = self.form_class(instance=user)
        teacher_form = self.teacher_form_class(instance=teacher)
        context['user_form'] = user_form
        context['teacher_form'] = teacher_form
        return context

    def form_valid(self, form):
        # First, handle the CustomUserChangeForm
        response = super().form_valid(form)
        user = self.get_object().user
        teacher = self.get_object()
        
        # Process and save the StudentForm
        teacher_form = self.teacher_form_class(self.request.POST, instance=teacher)
        user_form = self.form_class(self.request.POST, instance=user)
        if teacher_form.is_valid() and user_form.is_valid():
            user_form.save()
            teacher_form.save()
            print("Student form saved.")
        else:
            print("Student form errors:", teacher_form.errors)
        return response

    def form_invalid(self, form):
        print("Form invalid.")
        teacher = self.get_object()
        teacher_form = self.teacher_form_class(self.request.POST, instance=teacher)
        return self.render_to_response(self.get_context_data(form=form, teacher_form=teacher_form))

    def get_success_url(self):
        return reverse('Admin:teacherlist')          

#  **************************************************************
#  ************************ Event *****************************
#  **************************************************************

class EventList(LoginRequiredMixin,ListView):
    model = Event
    template_name = 'Admin/admin-event.html'
    context_object_name = 'events'       

class AddEvent(LoginRequiredMixin,CreateView):
    template_name = 'Admin/admin-add-event.html'  
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('Admin:eventlist')   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context   

class DeleteEvent(LoginRequiredMixin,DeleteView):     
    model =  Event
    template_name = 'Admin/admin-event.html'
    success_url = reverse_lazy('Admin:eventlist') 

class EditEvent(LoginRequiredMixin,UpdateView): 
    template_name = 'Admin/admin-edit-event.html'
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('Admin:eventlist') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context

#  **************************************************************
#  ************************ Holiday *****************************
#  **************************************************************

class HolidayList(LoginRequiredMixin,ListView):
    model = Holiday
    template_name = 'Admin/admin-holiday.html'
    context_object_name = 'holidays'       

class AddHoliday(LoginRequiredMixin,CreateView):
    template_name = 'Admin/admin-add-holiday.html'  
    model = Holiday
    form_class = HolidayForm
    success_url = reverse_lazy('Admin:holidaylist')    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context   

class DeleteHoliday(LoginRequiredMixin,DeleteView):     
    model =  Holiday
    template_name = 'Admin/admin-holiday.html'
    success_url = reverse_lazy('Admin:holidaylist') 

class EditHoliday(LoginRequiredMixin,UpdateView): 
    template_name = 'Admin/admin-edit-holiday.html'
    model = Holiday
    form_class = HolidayForm
    success_url = reverse_lazy('Admin:holidaylist')      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context   

#  **************************************************************
#  *********************** Attendance  **************************
#  **************************************************************

class AttendenceList(LoginRequiredMixin,ListView):
    model = Attendance
    template_name = 'Admin/admin-attendence.html'
    context_object_name = 'attendance'   

#  **************************************************************
#  ************************** Exam ******************************
#  **************************************************************

class ExamList(LoginRequiredMixin,ListView):
    model = Exam
    template_name = 'Admin/admin-exam.html'
    context_object_name = 'exams'   

class AddExam(LoginRequiredMixin,CreateView):
    template_name = 'Admin/admin-add-exam.html'  
    model = Exam
    form_class = ExamForm
    success_url = reverse_lazy('Admin:examlist')      

class DeleteExam(LoginRequiredMixin,DeleteView):     
    model =  Exam
    template_name = 'Admin/admin-exam.html'
    success_url = reverse_lazy('Admin:examlist')   

class EditExam(LoginRequiredMixin,UpdateView): 
    template_name = 'Admin/admin-edit-exam.html'
    model = Exam
    form_class = ExamForm
    success_url = reverse_lazy('Admin:examlist')       

#  **************************************************************
#  ************************** Fees ******************************
#  **************************************************************

class FeesList(LoginRequiredMixin,ListView):
    model = Fees
    template_name = 'Admin/admin-fees.html'
    context_object_name = 'fees'    

class AddFees(LoginRequiredMixin,CreateView):
    template_name = 'Admin/admin-add-fees.html'  
    model = Fees
    form_class = FeesForm
    success_url = reverse_lazy('Admin:feeslist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context

    def form_valid(self, form):
        # Handle form validation and saving
        return super().form_valid(form)

    def form_invalid(self, form):
        # Render the form with errors
        return self.render_to_response(self.get_context_data(form=form))
    
class DeleteFees(LoginRequiredMixin,DeleteView):     
    model =  Fees
    template_name = 'Admin/admin-fees.html'
    success_url = reverse_lazy('Admin:feeslist')   

class EditFees(LoginRequiredMixin,UpdateView): 
    template_name = 'Admin/admin-edit-fees.html'
    model = Fees
    form_class = FeesForm
    success_url = reverse_lazy('Admin:feeslist') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context        

#  **************************************************************
#  ************************* Salary *****************************
#  **************************************************************

class SalaryList(LoginRequiredMixin,ListView):
    model = Salary
    template_name = 'Admin/admin-salary.html'
    context_object_name = 'salarys'

class AddSalary(LoginRequiredMixin,CreateView):
    template_name = 'Admin/admin-add-salary.html'  
    model = Salary
    form_class = SalaryForm
    success_url = reverse_lazy('Admin:salarylist')      

class DeleteSalary(LoginRequiredMixin,DeleteView):     
    model =  Salary
    template_name = 'Admin/admin-salary.html'
    success_url = reverse_lazy('Admin:salarylist')   

class EditSalary(LoginRequiredMixin,UpdateView): 
    template_name = 'Admin/admin-edit-salary.html'
    model = Salary
    form_class = SalaryForm
    success_url = reverse_lazy('Admin:salarylist')     

#  **************************************************************
#  ************************* Notice *****************************
#  **************************************************************

class NoticeList(LoginRequiredMixin,ListView):
    model = Notice
    template_name = 'Admin/admin-notice.html'
    context_object_name = 'notices'

class AddNotice(LoginRequiredMixin,CreateView):
    template_name = 'Admin/admin-add-notice.html'  
    model = Notice
    form_class = NoticeForm
    success_url = reverse_lazy('Admin:noticelist')      

class DeleteNotice(LoginRequiredMixin,DeleteView):     
    model =  Notice
    template_name = 'Admin/admin-notice.html'
    success_url = reverse_lazy('Admin:noticelist')   

class EditNotice(LoginRequiredMixin,UpdateView): 
    template_name = 'Admin/admin-edit-notice.html'
    model = Notice
    form_class = NoticeForm
    success_url = reverse_lazy('Admin:noticelist')                                                                                                                                                                                                                                                                                                                                                                               