# meals/urls.py
from django.urls import path
from .views import MealListView, MealDetailView, SearchResultsListView

urlpatterns = [
    path('', MealListView.as_view(), name="meal_list"),
    path('<uuid:pk>/', MealDetailView.as_view(), name="meal_detail"),
    path('search/', SearchResultsListView.as_view(), name="search_results"),
]