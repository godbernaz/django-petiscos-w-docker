# meals/admin.py
from django.contrib import admin
from .models import Meal, Category, Review

# Reviews Inline
class ReviewInline(admin.TabularInline):
    model = Review

# Meals Admin
class MealAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]
    list_display = ('meal_name', 'category', 'price',)

admin.site.register(Meal, MealAdmin)
admin.site.register(Category)