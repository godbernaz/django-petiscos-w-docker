# meals/urls.py
from django.urls import path
from .views import MealListView, MealDetailView

urlpatterns = [
    path('', MealListView.as_view(), name="meal_list"),
    path('<uuid:pk>/', MealDetailView.as_view(), name="meal_detail"),
]