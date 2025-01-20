# carts/urls.py
from django.urls import path
from .views import CartDetailsView, CartAddView, cart_delete, cart_update

urlpatterns = [
    path('', CartDetailsView.as_view(), name="cart_detail"),
    path('add/', CartAddView.as_view(), name="cart_add"),
    path('delete/', cart_delete.as_view(), name="cart_delete"),
    path('update/', cart_update.as_view(), name="cart_update"),
]
