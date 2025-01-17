# meals/views.py
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Meal, Category

class MealListView(ListView):
    model = Meal
    context_object_name = 'meal_list'
    template_name = 'meals/meal_list.html'
    
class MealDetailView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        DetailView):
    model = Meal
    context_object_name = 'meal'
    template_name = 'meals/meal_detail.html'
    login_url = 'account_login'
    permission_required = 'meals.special_status'

class SearchResultsListView(ListView):
    model = Meal
    context_object_name = 'meal_list'
    template_name = 'meals/search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Meal.objects.filter(
            Q(meal_name__icontains=query) | Q(category__category_name__icontains=query)
        )