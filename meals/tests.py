# meals/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from .models import Meal, Category,  Review

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
            user_review = cls.user,
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
        
    def test_meal_detail_view(self):
        response = self.client.get(self.meal.get_absolute_url())
        no_response = self.client.get('/meals/12345')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Francesinha')
        self.assertContains(response, 'Fantastico Lininha')
        self.assertTemplateUsed(response, 'meals/meal_detail.html')
