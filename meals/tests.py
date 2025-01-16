# meals/tests.py
from django.test import TestCase
from django.urls import reverse

from .models import Meal, Category

class MealTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            category_name='Filetes'
        )
        cls.meal = Meal.objects.create(
            meal_name='Francesinha',
            category=cls.category,
            price='30.00',
            description='ola', 
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
        
    def test_meal_detail_view(self):
        response = self.client.get(self.meal.get_absolute_url())
        no_response = self.client.get('/meals/12345')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Francesinha')
        self.assertTemplateUsed(response, 'meals/meal_detail.html')
