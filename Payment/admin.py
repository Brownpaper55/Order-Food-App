from django.contrib import admin
from .models import Delivery_Address, Order, OrderItem

# Register your models here.
admin.site.register(Delivery_Address)
admin.site.register(Order)
admin.site.register(OrderItem)

#create an orderitem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['user','full_name','amount_paid','delivered','date_delivered']
    inlines = [OrderItemInline]

#unregister order model
admin.site.unregister(Order)

#Re-register order model
admin.site.register(Order, OrderAdmin)