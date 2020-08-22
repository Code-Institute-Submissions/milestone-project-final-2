from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
import uuid
from products.models import Product
from django.contrib.auth.models import User
from profiles.models import Profile

# Create your models here.

class Order(models.Model):
    """
    The Order model stores information about the user's name,
    phone number and address  to assist in the delivery of products
    """
    order_number = models.CharField(max_length=32, null=True, editable=False)
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=True, blank=False, default=None)
    email = models.EmailField(max_length=254, null=True, blank=False, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=False, default=None)
    street_address = models.CharField(max_length=100, null=True, blank=False, default=None)
    address2 = models.CharField(max_length=80, null=True, blank=True, default=None)
    country = CountryField(blank_label='Country *', multiple=False, null=False, blank=False, default=None)
    town_or_city = models.CharField(max_length=100, null=True, default=None)
    postcode = models.CharField(max_length=100, null=True, default=None)
    date = models.DateTimeField(null=True, default=None)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    final_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        """
        Update total each time an item is added, including delivery costs.
        """
        self.order_total = self.order_item.aggregate(Sum('item_total'))['item_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.final_total = self.order_total + self.delivery_cost
        self.save()
        
    def save(self, *args, **kwargs):
        """
        Set the order number if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)   
    quantity = models.IntegerField(blank=True)
    item_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False, default=None)
    
    def save(self, *args, **kwargs):
        """
        Update the order total.
        """
        self.item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
        
        