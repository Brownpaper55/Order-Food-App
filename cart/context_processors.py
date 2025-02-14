from .cart import Cart
#creating context processor that can work on all pages
def cart(request):
    #return the default data from our cart
    return{'cart':Cart(request)}