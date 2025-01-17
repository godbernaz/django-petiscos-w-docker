# meals/tests.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Meal, Category, Review

class MealTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='reviewuser',
            email='reviewuser@email.com',
            password='testpass123',
        )
        
        cls.category = Category.objects.create(
            category_name='Filetes'
        )
        
        cls.meal = Meal.objects.create(
            meal_name='Francesinha',
            category=cls.category,
            price='30.00',
            description='ola', 
        )
        
        cls.review = Review.objects.create(
            meal=cls.meal,
            user_review=cls.user,
            review='Fantastico Lininha',
        )
        
    def test_meal_listing(self):
        self.assertEqual(f"{self.meal.meal_name}", 'Francesinha')
        self.assertEqual(f"{self.meal.category.category_name}", 'Filetes')
        self.assertEqual(f"{self.meal.price}", '30.00')
        self.assertEqual(f"{self.meal.description}", 'ola')
        
    def test_meal_list_view(self):
        response = self.client.get(reverse('meal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Francesinha')
        self.assertTemplateUsed(response, 'meals/meal_list.html')
        
    def test_meal_detail_view_for_logged_in_users_without_permission(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        response = self.client.get(self.meal.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    def test_meal_detail_view_for_logged_in_users_with_permission(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        special_permission = Permission.objects.get(codename='special_status')
        self.user.user_permissions.add(special_permission)
        response = self.client.get(self.meal.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Francesinha')
        self.assertContains(response, 'Fantastico Lininha')
        self.assertTemplateUsed(response, 'meals/meal_detail.html')
