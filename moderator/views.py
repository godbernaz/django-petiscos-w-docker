from django.views.generic import ListView
from django.views import View
from django.shortcuts import redirect
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from orders.models import Order

class ModView(UserPassesTestMixin, ListView):
    model = Order
    template_name = 'mod/mod_dashboard.html'
    context_object_name = 'orders'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        queryset = Order.objects.select_related('user', 'billing_info').all()

        # Get the date filter from the request
        filter_date = self.request.GET.get('date')
        if filter_date:
            parsed_date = parse_date(filter_date)
            if parsed_date:
                queryset = queryset.filter(created_at__date=parsed_date)

        return queryset

    def post(self, request, *args, **kwargs):
        """ Handle status updates via form submission. """
        try:
            data = request.POST
            
            for order in Order.objects.all():
                new_status = data.get(f"status_{order.id}")
                if new_status and new_status in dict(Order.STATUS_CHOICES) and order.status != new_status:
                    order.status = new_status
                    order.save()

            # Redirect back to the same page instead of returning JSON
            return redirect("mod_dashboard")  

        except Exception as e:
            return redirect("mod_dashboard")  