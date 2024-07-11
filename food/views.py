from django.shortcuts import render
from django.http import HttpResponse
from .models import Pizza
# Create your views here.

def index(request):
    return render(request, 'food/index.html')

def pizza_view(request):
    pizzas = Pizza.objects.all()
    ctx = {
        'pizzas': pizzas
    }
    print(pizzas)
    return render(request, 'food/pizza.html', ctx)