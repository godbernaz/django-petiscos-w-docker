# accounts/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import CustomUser, UserBilling
from django import forms
import re

from core.validators import PasswordNoSpecialCharactersValidator, PasswordNotCommonValidator, CustomPasswordValidator, PasswordNoCommonWordsValidator

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
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Apelido',
            'email': 'Email',
        }

class ChangePasswordForm(SetPasswordForm):
    old_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Palavra-passe antiga',
        }),
    )

    new_password1 = forms.CharField(
        label='Nova palavra-passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Palavra-passe nova',
        }),
        validators=[
            PasswordNoSpecialCharactersValidator().validate,
            PasswordNotCommonValidator().validate,
            CustomPasswordValidator().validate,
            PasswordNoCommonWordsValidator().validate,
        ]
    )

    new_password2 = forms.CharField(
        label='Confirmar palavra-passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar palavra-passe nova',
        }),
    )

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        field_attrs = {
            'new_password1': {
                'placeholder': 'Palavra-passe nova',
            },
            'new_password2': {
                'placeholder': 'Confirmar palavra-passe nova',
            },
        }

        for field_name, attrs in field_attrs.items():
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-control', 'placeholder': attrs['placeholder']})
            field.label = ''

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.user  

        if not check_password(old_password, user.password):
            raise forms.ValidationError('A palavra-passe antiga não está correta. Por favor, tenta novamente.')
        
        return old_password
        
class UserBillingForm(forms.ModelForm):
    class Meta:
        model = UserBilling
        fields = ['name', 'address', 'postal_code', 'city', 'phone', 'nif', 'is_default']
        labels = {
            'name': 'Nome do Perfil',
            'address': 'Morada',
            'city': 'Cidade',
            'postal_code': 'Código Postal',
            'phone': 'Telemóvel',
            'nif': 'NIF',
            'is_default': 'Definir como padrão',
        }

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if postal_code and not re.match(r'^\d{4}-\d{3}$', postal_code):
            raise forms.ValidationError("O código postal deve estar no formato XXXX-XXX.")
        return postal_code

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and (not phone.isdigit() or len(phone) != 9):
            raise forms.ValidationError("O número de telemóvel deve conter exatamente 9 dígitos e apenas números.")
        return phone

    def clean_nif(self):
        nif = self.cleaned_data.get('nif')
        if nif and (not nif.isdigit() or len(nif) != 9):
            raise forms.ValidationError("O NIF deve conter exatamente 9 dígitos e apenas números.")
        return nif