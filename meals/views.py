# meals/views.py
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    #PermissionRequiredMixin
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Meal, Category

@method_decorator(login_required, name='dispatch')
class MealListView(ListView):
    model = Meal
    context_object_name = 'meal_list'
    template_name = 'meals/meal_list.html'

@method_decorator(login_required, name='dispatch')
class MealDetailView(DetailView):
    model = Meal
    context_object_name = 'meal'
    template_name = 'meals/meal_detail.html'
    login_url = 'account_login'
    queryset = Meal.objects.all().prefetch_related('reviews__user_review',)

class SearchResultsListView(ListView):
    model = Meal
    context_object_name = 'meal_list'
    template_name = 'meals/search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Meal.objects.filter(
            Q(meal_name__icontains=query) | Q(category__category_name__icontains=query)
        )