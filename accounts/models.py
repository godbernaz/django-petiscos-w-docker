# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=40, blank=True, null=True)
    postal_code = models.CharField(
        max_length=8,  
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{4}-\d{3}$',
                message='O código postal deve estar no formato XXXX-XXX.'
            )
        ]
    )
    city = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    nif = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{9}$',
                message='O NIF deve conter exatamente 9 dígitos.'
            )
        ]
    )
