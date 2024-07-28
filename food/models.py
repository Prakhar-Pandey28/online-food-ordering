from django.db import models
from django.contrib.auth.models import User

class Pizza(models.Model):
    name = models.CharField(max_length=120)
    priceM = models.DecimalField(max_digits=4, decimal_places=2)
    priceL = models.DecimalField(max_digits=4, decimal_places=2)
    pImage = models.URLField()

    def __str__(self):
        return self.name

class Burger(models.Model):
    name = models.CharField(max_length=120)
    priceM = models.DecimalField(max_digits=4, decimal_places=2)
    priceL = models.DecimalField(max_digits=4, decimal_places=2)
    bImage = models.URLField()

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=60, unique=True)
    bill = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField(auto_now_add=True, blank=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.number} by {self.customer.username}"

class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    size = models.CharField(max_length=10)  # Added size field to reflect size of the pizza or burger

    def __str__(self):
        return f"{self.name} (Order: {self.order.number})"
