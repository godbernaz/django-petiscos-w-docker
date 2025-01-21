from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from meals.models import Meal, Category
from carts.models import Cart, CartItem
import json

class CartCRUDTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            category_name='Pizza'
        )
        
        cls.user = get_user_model().objects.create_user(
            username='testuser3', 
            password='testpass123'
        )
        
        cls.meal = Meal.objects.create(
            meal_name='Pizza', 
            category=cls.category,  
            price=20.00, 
            description='Delicious pizza'
        )
    
    def setUp(self):
        self.client.login(
            username='testuser3', 
            password='testpass123'
        )
    
    def test_add_to_cart(self):
        response = self.client.post(
            reverse('cart_add'),
            {'meal_id': self.meal.id, 'quantity': 2},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(json.loads(response.content)['message'], 'Refeição adicionada ao carrinho')
    
    def test_remove_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, meal=self.meal, quantity=2)
        
        response = self.client.post(
            reverse('cart_delete'),
            {'meal_id': self.meal.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 0)
        self.assertEqual(json.loads(response.content)['message'], 'Refeição removida do carrinho')
    
    def test_update_quantity(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, meal=self.meal, quantity=2)
        
        response = self.client.post(
            reverse('cart_update'),
            {'meal_id': self.meal.id, 'action': 'increment'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(json.loads(response.content)['message'], 'Quantidade atualizada com sucesso')
    
    def test_cart_detail_view(self):
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carts/cart_detail.html')
