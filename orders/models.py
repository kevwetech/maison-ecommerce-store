# orders/models.py
from django.db import models
from django.conf import settings
from products.models import Product



class DeliveryOption(models.Model):
    DELIVERY_TYPES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('same_day', 'Same Day'),
    ]
    name = models.CharField(max_length=100)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_days = models.CharField(max_length=50)  # e.g. "3-5 days"
    free_above = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # free if order above this
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

        

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_option = models.ForeignKey(DeliveryOption, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price


