from django.shortcuts import render, get_object_or_404
from .cart import Cart
from E_kitchen .models import Dishes
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_foods = cart.get_foods
    quantity = cart.get_quants
    total = cart.cart_total
    return render(request, 'cart/cart_summary.html', {'cart_foods':cart_foods, 'quantity':quantity, 'total':total})
    

def cart_add(request):
    #Get the cart
    cart = Cart(request)
    #test for post
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Dishes, id=product_id)
        #save to session
        cart.add(product=product, quantity=product_qty)
        #Get cart quantity
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty':cart_quantity})
        messages.success(request, ("Item has been added to cart!!"))
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity= product_qty)
        response = JsonResponse({'qty':product_qty})
        messages.success(request, ("Cart update successful!!"))
        return response
    
        

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request, "Item has been deleted!!")
        return response