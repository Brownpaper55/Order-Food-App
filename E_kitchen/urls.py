from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='home'),
    path('menu/',  views.menu_view, name ='menu'),
    path('food/<int:id>/', views.food_view, name='food'),
    
]