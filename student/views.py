from django.shortcuts import render,redirect
from django.views.generic import *
from custom_admin.models import *
from django.urls import reverse_lazy
from custom_admin.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from student.forms import *
from student.models import Demo
from sms_project import settings

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

class Demoview(View):
    def get(self, request):
        form = DemoForm()
        stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        return render(request, 'Admin/demo.html', {
            'form': form,
            'stripe_pk': stripe_publishable_key
        })

    def post(self, request):
        form = DemoForm(request.POST, request.FILES)
        if form.is_valid():
            # Save only if payment was already done via JS
            Demo.objects.create(
                text=form.cleaned_data['text'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                url=form.cleaned_data['url'],
                tel=form.cleaned_data['tel'],
                number=form.cleaned_data['number'],
                range=form.cleaned_data['range'],
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                datetime=form.cleaned_data['datetime'],
                month=form.cleaned_data['month'],
                week=form.cleaned_data['week'],
                checkbox1=form.cleaned_data['checkbox1'],
                checkbox2=form.cleaned_data['checkbox2'],
                radio=form.cleaned_data['radio'],
                file=form.cleaned_data['file'],
                select=form.cleaned_data['select'],
                textarea=form.cleaned_data['textarea'],
                hidden=form.cleaned_data['hidden'],
            )
            return redirect('Student:leavelist')
        else:
            stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
            return render(request, 'Admin/demo.html', {
                'form': form,
                'stripe_pk': stripe_publishable_key
            })

import stripe
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator   
class CreatePaymentIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY  # 🔥 This line is crucial
            data = json.loads(request.body)
            amount = data.get("amount", 1000)  # default to $10

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
            )
            return JsonResponse({"clientSecret": intent.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
  
@csrf_exempt
def save_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method_x = data.get('payment_method')
            amount = data.get('amount')
            print('payment_method_x:', payment_method_x)

            if payment_method_x == 'card':
                payment_intent_id = data.get('payment_intent_id')
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                payment_method_id = intent.payment_method
                payment_method = stripe.PaymentMethod.retrieve(payment_method_id)

                payment = Payment.objects.create(
                    payment_method='card',
                    amount=amount,
                    payment_intent_id=intent.id,
                    customer_id=intent.customer,
                    last_4_digits=payment_method.card.last4,
                    card_type=payment_method.card.brand,
                    expiration_date=f"{payment_method.card.exp_month}/{payment_method.card.exp_year}",
                    transaction_id=intent.id,
                    payment_status='success'
                )

            elif payment_method_x == 'cheque':
                print('payment_method_x: ', payment_method_x)
                # Cheque doesn't have Stripe payment data
                payment = Payment.objects.create(
                    payment_method='cheque',
                    amount=amount,
                    payment_status='pending'
                )

            else:
                return JsonResponse({"status": "error", "message": "Invalid payment method."})

            return JsonResponse({"status": "success", "payment_id": payment.id})

        except Exception as e:
            print("Error storing payment:", str(e))
            return JsonResponse({"status": "error", "message": str(e)})