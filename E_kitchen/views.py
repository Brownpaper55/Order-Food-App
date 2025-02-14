from django.shortcuts import render, get_object_or_404
from .models import Dishes, DishType

# Create your views here.
def index(request):
    offers = Dishes.objects.all()
    return render(request,'landing.html', {'offers':offers})


def menu_view(request):
    menu = Dishes.objects.all()
    return render(request, 'menu.html', {'menu':menu})

def food_view(request, id):
    food = get_object_or_404(Dishes, id=id)
    return render(request, 'food.html',{'food':food})
 