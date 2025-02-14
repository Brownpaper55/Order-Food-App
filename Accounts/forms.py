from django import forms
from .models import Customer
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm


class UpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = Customer
        fields  = ['new_password1', 'new_password2']


class CustomerRegistrationForm(UserCreationForm):
    firstname = forms.CharField(max_length=50, required= True)
    lastname = forms.CharField(max_length=50, required= True)
    email = forms.EmailField(required=True, help_text= 'Enter a valid Email address')
    password =forms.PasswordInput()
    class Meta:
        model = Customer
        fields= ('firstname', 'lastname','username','email','phone', 'city','address')


class CustomerChangeForm(UserChangeForm):
    firstname = forms.CharField(max_length=50, required= True)
    lastname = forms.CharField(max_length=50, required= True)
    email = forms.EmailField(required=True, help_text= 'Enter a valid Email address')
    password = None
    class Meta:
        model = Customer
        fields= ('firstname', 'lastname','username','email','phone','city','address')


  