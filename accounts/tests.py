from django.test import TestCase
from django.contrib.auth import get_user_model

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