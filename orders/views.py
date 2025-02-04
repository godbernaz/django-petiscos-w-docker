from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from carts.models import Cart
from accounts.models import UserBilling
from accounts.forms import UserBillingForm

class OrderDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        billing_profiles = UserBilling.objects.filter(user=self.request.user)
        form = UserBillingForm()
        
        context['cart'] = cart
        context['billing_profiles'] = billing_profiles
        context['billing_form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = UserBillingForm(request.POST)
        if form.is_valid():
            billing_profile = form.save(commit=False)
            billing_profile.user = request.user
            billing_profile.save()
            return redirect('order_detail')
        
        context = self.get_context_data()
        context['billing_form'] = form
        return self.render_to_response(context)

