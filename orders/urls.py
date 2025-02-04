# orders/urls.py
from django.urls import path
from .views import OrderDetailsView, ConfirmOrderView, OrderSuccessView

urlpatterns = [
    path('details/', OrderDetailsView.as_view(), name="order_detail"),
    path('orders/confirm/', ConfirmOrderView.as_view(), name='confirm_order'),
    path('success/<uuid:order_id>/', OrderSuccessView.as_view(), name="order_success"),
]