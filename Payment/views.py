from django.shortcuts import render,redirect
from cart.cart import Cart
from .models import Delivery_Address
from .forms import DeliveryForm, BillingForm
from .models import Order, OrderItem
from django.contrib import messages
from Accounts.models import Customer
import datetime

# Create your views here.

def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id = pk)
        items = OrderItem.objects.filter(order = pk)

        #toggling delivery status
        if request.POST:
            status = request.POST['delivery_status']
            if status == 'true':
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(delivered=True, date_delivered=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(delivered=False)
            messages.success(request,'Delivery status has been updated')
            return redirect('delivered')
        
        return render(request, 'payment/orders.html', {'order':order, 'items':items})
    else:
        messages.success(request,'Access denied')
        return redirect('home')

def delivered_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(delivered = True)
        return render(request,'payment/delivered_dashboard.html', {'order':orders})
    else:
        messages.success(request,"Access denied")
        return redirect('home')
    

def undelivered_dashboard(request):
     if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(delivered = False)
        return render(request,'payment/undelivered_dashboard.html',{'order':orders})
     else:
        messages.success(request,"Access denied")
        return redirect('home')
    
    



def process_order(request):
    if request.POST:
        #reuse cart methods
        cart = Cart(request)
        cart_foods = cart.get_foods
        quantity = cart.get_quants
        totals = cart.cart_total()
        #Grab info from page
        payment_form = BillingForm(request.POST or None)
        delivery_info = request.session.get('delivery_info')
        full_name = delivery_info['full_name']
        Delivery_address = f"{delivery_info['email']}\n{delivery_info['City']}\n{delivery_info['Address']}\n{delivery_info['Telephone']}"
        amount_paid = totals
        if request.user.is_authenticated:
            user = request.user
            #create order
            create_order = Order(user = user, full_name=full_name, Delivery_address = Delivery_address, amount_paid=amount_paid)
            create_order.save()

            #create order item
            order_id= create_order.pk
            for foods in cart_foods():
                foods_id = foods.id
                foods_price = foods.price
            # get quantity
                for key,value in quantity().items():
                    if int(key) == foods.id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id,dish_id= foods_id, user=user,quantity=value,price=foods_price)
                        create_order_item.save()

            #delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            #empty database
            customer = Customer.objects.filter(id = request.user.id)
            customer.update(old_cart='')

            messages.success(request,"Order placed")
            return redirect('home')
        else:
            #if user is not authenticated
            create_order = Order(full_name=full_name, Delivery_address = Delivery_address, amount_paid=amount_paid)
            create_order.save()
            order_id= create_order.pk
            for foods in cart_foods():
                foods_id = foods.id
                foods_price = foods.price
            # get quantity
                for key,value in quantity().items():
                    if int(key) == foods.id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id,dish_id= foods_id, quantity=value,price=foods_price)
                        create_order_item.save()

            #delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
           
            messages.success(request,"Order placed")
            return redirect('home')


        
    else:
        messages.success(request,"Access denied")
        return redirect('home')

def billing(request):
    if request.POST:
        cart = Cart(request)
        cart_foods = cart.get_foods
        quantity = cart.get_quants
        total = cart.cart_total
        delivery_info = request.POST
        request.session['delivery_info'] = delivery_info
        if request.user.is_authenticated:
            bill_form = BillingForm()
            return render(request, 'payment/billing.html',{'cart_foods':cart_foods, 'quantity':quantity, 'total':total, 'Billing_info':request.POST,'form':bill_form})
        else:
           bill_form = BillingForm()
           return render(request, 'payment/billing.html',{'cart_foods':cart_foods, 'quantity':quantity, 'total':total, 'Billing_info':request.POST,'form':bill_form})
    else:
        messages.success(request,"Access denied") 
        return redirect ('home')   

def payment_success(request):
    return render(request,'payment/payment_success.html')

def checkout(request):
    cart = Cart(request)
    cart_foods = cart.get_foods
    quantity = cart.get_quants
    total = cart.cart_total

    if request.user.is_authenticated:
        #Checkout as user
        Delivery_user  = Delivery_Address.objects.get(user_id=request.user.id)
        form = DeliveryForm(request.POST or None, instance= Delivery_user )
        return render(request, 'payment/checkout.html', {'cart_foods':cart_foods, 'quantity':quantity, 'total':total, 'form':form} )
    else:
        #checkout as guest
        form = DeliveryForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_foods':cart_foods, 'quantity':quantity, 'total':total, 'form':form})
    