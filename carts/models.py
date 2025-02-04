# carts/models.py
from django.db import models
from django.contrib.auth import get_user_model
from meals.models import Meal  # Importa o modelo de refeição

class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        on_delete=models.CASCADE
    )  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"
    
    @property
    def total_cart_price(self):
        return sum(item.total_price for item in self.items.all())  

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)  
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)  

    def __str__(self):
        return f"{self.quantity} x {self.meal.meal_name} in {self.cart.user.username}'s cart"

    class Meta:
        unique_together = ('cart', 'meal')  

    @property
    def total_price(self):
        return self.meal.price * self.quantity  