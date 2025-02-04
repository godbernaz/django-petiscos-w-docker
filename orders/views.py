from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from carts.models import Cart
from accounts.models import UserBilling
from accounts.forms import UserBillingForm
from orders.models import Order, OrderItem

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
        if 'billing_profile' in request.POST:
            billing_profile_id = request.POST.get('billing_profile')
            billing_profile = get_object_or_404(UserBilling, id=billing_profile_id, user=request.user)
            return redirect('confirm_order', billing_profile_id=billing_profile.id)
        
        form = UserBillingForm(request.POST)
        if form.is_valid():
            billing_profile = form.save(commit=False)
            billing_profile.user = request.user
            billing_profile.save()
            return redirect('order_detail')
        
        context = self.get_context_data()
        context['billing_form'] = form
        return self.render_to_response(context)

class ConfirmOrderView(LoginRequiredMixin, View):
    def post(self, request):
        billing_profile_id = request.POST.get('billing_profile')
        cart = get_object_or_404(Cart, user=request.user)
        billing_profile = get_object_or_404(UserBilling, id=billing_profile_id, user=request.user)

        if not cart.items.exists():
            return redirect('order_detail')

        order = Order.objects.create(
            user=request.user,
            billing_info=billing_profile,
            total_price=cart.total_cart_price
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                meal=item.meal,
                quantity=item.quantity,
                price=item.meal.price
            )

        cart.items.all().delete()
        return redirect('order_success', order_id=order.id)

class OrderSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, id=self.kwargs['order_id'], user=self.request.user)
        return context
