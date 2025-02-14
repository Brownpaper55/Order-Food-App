from django import forms
from .models import Delivery_Address


class DeliveryForm(forms.ModelForm):
    full_name = forms.CharField(max_length=255,  required=True)
    email = forms.EmailField(max_length=255, required= True)
    City = forms.CharField(max_length=255, required=True)
    Address = forms.CharField(max_length=255, required= True)
    Telephone = forms.CharField(max_length=255, required=True)
    class Meta:
        model = Delivery_Address
        fields = ['full_name','email', 'City','Address','Telephone']
        exclude = ['user',]


class BillingForm(forms.Form):
    card_name = forms.CharField(max_length=20, required=True)
    card_number = forms.CharField(max_length=20, required=True)
    expiry_date = forms.DateField(required=True)
    card_cvv_number = forms.CharField(max_length=20, required=True)