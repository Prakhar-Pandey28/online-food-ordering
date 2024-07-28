from django.test import TestCase
from django.urls import reverse
from .models import Pizza

# Create your tests here.
class homePageTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class PizzaTestCase(TestCase):
    def test_newPizza_added(self):
        numPizza = Pizza.objects.count()
        Pizza.objects.create(name='Pizza', priceM=5.99, priceL= 8, pImage="someUrl")
        self.assertEqual(Pizza.objects.count(), numPizza+1)