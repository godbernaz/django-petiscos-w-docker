# carts/urls.py
from django.urls import path
from .views import CartDetailsView, CartAddView, CartDeleteView, CartUpdateView

urlpatterns = [
    path('', CartDetailsView.as_view(), name="cart_detail"),
    path('add/', CartAddView.as_view(), name="cart_add"),
    path('delete/', CartDeleteView.as_view(), name="cart_delete"),
    path('update/', CartUpdateView.as_view(), name="cart_update"),
]
