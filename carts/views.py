# carts/views.py
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import TemplateView

from meals.models import Meal
from .models import Cart, CartItem

class CartDetailsView(TemplateView):
    template_name = 'carts/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        context['cart'] = cart
        context['cart_item_count'] = cart.items.count()  
        return context

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

@method_decorator(login_required, name='dispatch')
class CartDeleteView(View):
    def post(self, request, *args, **kwargs):
        meal_id = self.request.POST.get('meal_id')
        meal = get_object_or_404(Meal, id=meal_id)
        cart = get_object_or_404(Cart, user=request.user)

        try:
            cart_item = CartItem.objects.get(cart=cart, meal=meal)
            cart_item.delete()
            return JsonResponse({'message': 'Refeição removida do carrinho', 'cart_quantity': cart.items.count()})
        except CartItem.DoesNotExist:
            return JsonResponse({'message': 'Refeição não encontrada no carrinho'}, status=404)

@method_decorator(login_required, name='dispatch')
class CartUpdateView(View):
    def post(self, request, *args, **kwargs):
        meal_id = self.request.POST.get('meal_id')
        action = self.request.POST.get('action')

        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, meal_id=meal_id)

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

        return JsonResponse({
            'message': 'Quantidade atualizada com sucesso',
            'cart_quantity': cart.items.count()
        })