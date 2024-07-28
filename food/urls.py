from django.urls import path
from . import views

app_name = 'food'

urlpatterns = [
    path('', views.index, name='index'),
    path('pizza/', views.pizza_view, name='pizza_view'),
    path('burgers/', views.burger_view, name='burger_view'),
    path('order/', views.order_view, name='order'),
    path('create-payment/', views.create_payment, name='create_payment'),
    path('success/', views.success, name='success'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
]
