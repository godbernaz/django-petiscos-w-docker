# accounts/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'username',
        )
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'username',
        )
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'date_of_birth',
        ]
        
class UserAddressForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'address', 'postal_code', 'city', 'phone', 'nif'
        ]
        
    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        
        if not postal_code or not re.match(r'^\d{4}-\d{3}$', postal_code):
            raise forms.ValidationError("O código postal deve estar no formato XXXX-XXX.")
        
        return postal_code
    
    def clean_nif(self):
        nif = self.cleaned_data.get('nif')
        if nif and not nif.isdigit():
            raise forms.ValidationError('O NIF deve conter apenas números.')
        if len(nif) != 9:
            raise forms.ValidationError('O NIF deve conter exatamente 9 dígitos.')
        return nif