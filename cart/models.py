from django.db import models
from E_kitchen.models import Dishes
from Accounts.models import Customer

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Cart for {self.user.username}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="Items")
    food_item = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} +' '+ {self.food_item.name}"
    
    def get_total_price(self):
        return self.quantity * self.food_item.price
