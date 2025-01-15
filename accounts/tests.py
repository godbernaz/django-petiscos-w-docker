from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve


# Create your tests here.
class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="bernaz", email="bernaz@email.com", password="123teste123"
        )
        self.assertEqual(user.username, "bernaz")
        self.assertEqual(user.email, "bernaz@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="superadmin", email="superadmin@email.com", password="123teste123"
        )
        self.assertEqual(admin_user.username, "superadmin")
        self.assertEqual(admin_user.email, "superadmin@email.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        
    def test_password_is_encrypted(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", email="test@email.com", password="testpass123"
        )
        self.assertTrue(user.check_password("testpass123"))  # Checks that the password has been encrypted correctly
        
class SignUpPageTests(TestCase):
    username = 'newuser'
    email = 'newuser@email.com'
    
    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)
    
    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Criar")
        self.assertNotContains(self.response, "I dont exist here!")
        
    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
        
    
    