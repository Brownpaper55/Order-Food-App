from django.db import models

# Create your models here.

class DishType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Dishes(models.Model):
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)

    def __str__(self):
        return self.name


