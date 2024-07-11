from django.urls import path
from . import views

app_name = 'food'

urlpatterns = [
    path('pizza/', views.pizza_view, name='pizza_view'),
]