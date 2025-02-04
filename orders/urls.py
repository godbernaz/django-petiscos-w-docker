# orders/urls.py
from django.urls import path
from .views import OrderDetailsView

urlpatterns = [
    path('details/', OrderDetailsView.as_view(), name="order_detail"),
]