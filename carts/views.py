from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from meals.models import Meal
from .models import Cart, CartItem
from django.http import JsonResponse
from django.views.generic import TemplateView

class CartDetailsView(TemplateView):
    template_name = 'carts/cart_detail.html'  # Especifique o caminho do seu template

@method_decorator(login_required, name='dispatch')
class CartAddView(View):
    def post(self, request, *args, **kwargs):
        meal_id = self.request.POST.get('meal_id')
        quantity = int(self.request.POST.get('quantity', 1))

        meal = get_object_or_404(Meal, id=meal_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, meal=meal)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        return JsonResponse({'message': 'Refeição adicionada ao carrinho', 'cart_quantity': cart.items.count()})

class cart_delete(TemplateView):
    pass

class cart_update(TemplateView):
    pass