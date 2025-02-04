from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from carts.models import Cart
from accounts.models import UserBilling

class OrderDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        billing_profiles = UserBilling.objects.filter(user=self.request.user)
        
        context['cart'] = cart
        context['billing_profiles'] = billing_profiles
        return context
