# accounts/urls.py
from django.urls import path
from .views import UserProfileView, OrderListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='account_profile'),
    path('orders_list/', OrderListView.as_view(), name='order_list'),
]