# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

def validate_postal_code():
    return RegexValidator(
        regex=r'^\d{4}-\d{3}$',
        message='O código postal deve estar no formato XXXX-XXX.'
    )

def validate_phone():
    return RegexValidator(
        regex=r'^\d{9}$',
        message='O número de telemóvel deve conter exatamente 9 dígitos.'
    )

def validate_nif():
    return RegexValidator(
        regex=r'^\d{9}$',
        message='O NIF deve conter exatamente 9 dígitos.'
    )
    
class CustomUser(AbstractUser):
    pass
    
class UserBilling(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='billing_info')
    address = models.CharField(max_length=40, blank=True, null=True)
    postal_code = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        validators=[validate_postal_code()]
    )
    city = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(
        max_length=9,  
        blank=True,
        null=True,
        validators=[validate_phone()]
    )
    nif = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        validators=[validate_nif()]
    )