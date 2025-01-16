# meals/models.py
import uuid
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
    
    
    
