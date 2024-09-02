from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import *
from accounts.forms import *
from django.shortcuts import redirect
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from custom_admin.urls import *
from custom_admin.views import *
from django.contrib import messages

class Loginview(LoginView):
    model = CustomUser
    form_class = LoginForm
    template_name = 'Accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user:
            login(self.request, user)

            if user.user_type == 'Admin':
                return redirect(reverse_lazy('Admin:admindashboard'))
            elif user.user_type == 'Teachers':
                return redirect(reverse_lazy('Teacher:studentdashboard'))
            elif user.user_type == 'Student':
                return redirect(reverse_lazy('Student:studentdashboard'))
            else:
                return self.form_invalid(form)
        else:
            messages.error(self.request, 'Invalid Login ID or password')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Login ID or password')
        return super().form_invalid(form)
    
class LogOut(LoginRequiredMixin, LogoutView):
    """
    A class-based view for logging out users with custom behavior.
    """
    next_page = reverse_lazy('Accounts:login')