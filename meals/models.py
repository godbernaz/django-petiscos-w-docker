# meals/models.py
import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

# Meals Categories
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
	    verbose_name_plural = 'Categories'

# Meals Model
class Meal(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    meal_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.meal_name
    
    def get_absolute_url(self):
        return reverse('meal_detail', args=[str(self.id)])
    
class Review(models.Model):
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    
    review = models.CharField(max_length=255)
    user_review = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
         return self.review
    
    
