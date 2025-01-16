from django.contrib import admin
from .models import Meal, Category

# How Meals Interface will appear in /admin/
class MealAdmin(admin.ModelAdmin):
    list_display = ('meal_name', 'category', 'price',)

admin.site.register(Meal, MealAdmin)
admin.site.register(Category)