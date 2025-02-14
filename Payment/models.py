from django.db import models
from Accounts.models import Customer
from E_kitchen.models import Dishes
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime 

# Create your models here.
class Delivery_Address(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    City = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    Telephone = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural  = "Delivery_Address"

    def __str__(self):
        return f"Delivery Address{str(self.id)}"
    
    #Create a user delivery address by default
    def create_delivery(sender, instance, created, **kwargs):
        if created:
            user_delivery = Delivery_Address(user=instance)
            user_delivery.save()
    #Automate the profile thing
    post_save.connect(create_delivery, sender = Customer)
    

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=250)
    Delivery_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    date_delivered = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order -{str(self.id)}"
    
    #Auto add delivery date
@receiver(pre_save, sender= Order)
def set_delivery_date(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.delivered and not obj.delivered:
            instance.date_delivered = now


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Order -{str(self.id)}"
