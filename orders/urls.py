# orders/urls.py
from django.urls import path
from .views import OrderListView, OrderDetailView, CheckoutDetailsView, ConfirmOrderView, OrderSuccessView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name="orders_list"),
    path('orders/<uuid:order_id>/', OrderDetailView.as_view(), name="order_detail"),
    path('checkout/', CheckoutDetailsView.as_view(), name="checkout"),
    path('orders/confirm/', ConfirmOrderView.as_view(), name='confirm_order'),
    path('success/<uuid:order_id>/', OrderSuccessView.as_view(), name="order_success"),
]