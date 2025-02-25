# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='billing_profiles')
    name = models.CharField(max_length=50, help_text="Nome do perfil de faturação", null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=8, blank=True, null=True, validators=[validate_postal_code()])
    phone = models.CharField(max_length=9, blank=True, null=True, validators=[validate_phone()])
    nif = models.CharField(max_length=9, blank=True, null=True, validators=[validate_nif()])
    is_default = models.BooleanField(default=False, help_text="Definir como perfil de faturação padrão")
    
    def save(self, *args, **kwargs):
        if self.is_default:
            UserBilling.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.nif}"
    
@receiver(pre_save, sender=CustomUser)
def ensure_single_email(sender, instance, **kwargs):
    if instance.pk:  
        old_email = CustomUser.objects.filter(pk=instance.pk).values_list('email', flat=True).first()
        if old_email and old_email != instance.email:
            # Remove old emails associated with the user
            EmailAddress.objects.filter(user=instance).delete()