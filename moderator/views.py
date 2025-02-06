from django.views.generic import ListView
from orders.models import Order
from django.contrib.auth.mixins import UserPassesTestMixin

class ModView(UserPassesTestMixin, ListView):
    model = Order
    template_name = 'mod/mod_dashboard.html'
    context_object_name = 'orders'

    def test_func(self):
        # Ensure only staff or superusers can access this view
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        # Fetch all orders and prefetch related data for better performance
        return Order.objects.select_related('user', 'billing_info').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context if needed
        return context