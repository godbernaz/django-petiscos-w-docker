# orders/models.py
from django.db import models
from django.conf import settings
from meals.models import Meal
from accounts.models import UserBilling
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Ready', 'Ready'),
        ('Delivered', 'Delivered'),
        ('Closed', 'Closed'),
        ('Canceled', 'Canceled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    billing_info = models.ForeignKey(UserBilling, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')

    def __str__(self):
        return f"Order {self.id} ({self.status}) by {self.user.username}"

    def calculate_total_price(self):
        self.total_price = sum(item.total_price for item in self.items.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.meal.meal_name} in Order {self.order.id}"
    
    @property
    def total_price(self):
        return self.price * self.quantity