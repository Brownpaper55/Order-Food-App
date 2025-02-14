from E_kitchen.models import Dishes
from Accounts.models import Customer

class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request

        #Get the current session key if it exists
        cart = self.session.get('session_key')

        #if the user is new, no session key create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available on all pages of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
           # self.cart[product_id] = {'name':str(product.name)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
        #Deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Customer.objects.filter(email=self.request.user.email)
            cartstring = str(self.cart)
            cartstring.replace("\'","\"")
            current_user.update(old_cart= cartstring)

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
           # self.cart[product_id] = {'name':str(product.name)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
        #Deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Customer.objects.filter(email=self.request.user.email)
            cartstring = str(self.cart)
            cartstring.replace("\'","\"")
            current_user.update(old_cart= cartstring)


    def __len__(self):
        return len(self.cart)
    

    def get_foods(self):
        #get the ids in our session dictionary
        product_ids = self.cart.keys()
        foods = Dishes.objects.filter(id__in=product_ids)
        return foods
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        cart = self.cart
        cart[product_id] = product_qty
        self.session.modified = True
        return self.cart
    
    def delete(self, product):
        product_id = str(product)
        cart = self.cart
        del(cart[product_id])

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Customer.objects.filter(email=self.request.user.email)
            cartstring = str(self.cart)
            cartstring.replace("\'","\"")
            current_user.update(old_cart= cartstring)



    def cart_total(self):
        product_ids = self.cart.keys()
        products = Dishes.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total += (product.price * value)
        return (total)