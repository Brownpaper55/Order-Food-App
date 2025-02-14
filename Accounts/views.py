from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerRegistrationForm, CustomerChangeForm, UpdatePasswordForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.views.generic.edit import CreateView
import json
from cart.cart import Cart
from Payment.forms import DeliveryForm
from Payment.models import Delivery_Address

# Create your views here.

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password Update Successful")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
            
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, 'registration/update_password.html',{'form':form})
    else:
        messages.success(request, "You must be signed in to view form")
        return redirect('home')


def update_user(request):
     if request.user.is_authenticated:
         current_user = Customer.objects.get(id=request.user.id)
         #Get current user delivery info
         Delivery_user  = Delivery_Address.objects.get(user_id=request.user.id)
         user_form = CustomerChangeForm(request.POST or None, instance = current_user)
         #Get user dedlivery form
         Delivery_form = DeliveryForm(request.POST or None, instance = Delivery_user)
         if user_form.is_valid and Delivery_form.is_valid():
             user_form.save()
             Delivery_form.save()
             login(request,current_user)
             messages.success(request, 'Your Profile has been updated!')
             return redirect('home')
         return render(request, 'registration/update_user.html', {'form':user_form, 'Delivery_form':Delivery_form})
     else:
         messages.success(request,'You must be logged in!')
         return redirect('login')
     


class UserSignupView(CreateView):
    form_class = CustomerRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'User has been created successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Invalid field detected!')
        return super().form_invalid(form)

"""def register_user(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form .is_valid():
            form.save()
            messages.success(request, 'Account has been created successfully')
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration/register.html', {'form':form})"""


def login_user(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request,f"Welcome {username}!!")
            login(request, user)
            #Get available items in shopping cart 
            saved_cart = user.old_cart
            #converting old_cart from string to dictionary
            if saved_cart:
                saved_cart = saved_cart.replace('\'','\"')
                converted_cart  = json.loads(saved_cart)
                cart = Cart(request)
                #Retrieve items from dictionary
                for key,value in converted_cart.items():
                    cart.db_add(product= key, quantity= value)


            return redirect('home')
        else:
            messages.error(request,"Invalid username or password!")
            return redirect('login')
    return render(request,'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')






