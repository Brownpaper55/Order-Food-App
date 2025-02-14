from django.urls import path
from . import views


urlpatterns = [
    path('payment_success/', views.payment_success, name= 'payment_sucess'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('billing_info/', views.billing, name = 'billing_info'),
    path('process_order/',views.process_order, name='process_order'),
    path('delivery_dashboard', views.delivered_dashboard, name = 'delivered'),
    path('undelivered_dashboard', views.undelivered_dashboard, name = 'undelivered'),
    path('orders/<int:pk>', views.orders, name = 'orders')
]