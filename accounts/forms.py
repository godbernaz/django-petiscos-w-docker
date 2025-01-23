# accounts/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import CustomUser, UserBilling
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
            'first_name', 'last_name', 'email',
        ]

class ChangePasswordForm(SetPasswordForm):
    old_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password Antiga',
        }),
        help_text=(
            '<span class="form-text text-muted">'
            '<small>Introduza a sua palavra-chave atual.</small>'
            '</span>'
        ),
    )

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        
        field_attrs = {
            'new_password1': {
                'placeholder': 'Palavra-chave nova',
                'help_text': (
                    '<ul class="form-text text-muted small">'
                    '<li>A sua palavra-chave não pode ser demasiado semelhante às suas outras informações pessoais.</li>'
                    '<li>A sua palavra-chave deve conter pelo menos 8 caracteres.</li>'
                    '<li>A sua palavra-chave não pode ser uma palavra-chave comummente utilizada.</li>'
                    '<li>A sua palavra-chave não pode ser totalmente numérica.</li>'
                    '</ul>'
                ),
            },
            'new_password2': {
                'placeholder': 'Confirmar palavra-chave nova',
                'help_text': (
                    '<span class="form-text text-muted">'
                    '<small>Introduza a mesma palavra-chave que anteriormente, para verificação.</small>'
                    '</span>'
                ),
            },
        }

        for field_name, attrs in field_attrs.items():
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-control', 'placeholder': attrs['placeholder']})
            field.label = ''
            field.help_text = attrs['help_text']

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.user  

        if not check_password(old_password, user.password):
            raise forms.ValidationError('A palavra-chave antiga não está correta. Por favor, tente novamente.')
        
        return old_password
        
class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserBilling
        fields = [
            'address', 'postal_code', 'city', 'phone', 'nif'
        ]
        
    # Check that the postal code is in the correct format (XXXX-XXX)
    def validate_postal_code_format(self):
        postal_code = self.cleaned_data['postal_code']
        if not postal_code or not re.match(r'^\d{4}-\d{3}$', postal_code):
            raise forms.ValidationError("O código postal deve estar no formato XXXX-XXX.")
        return postal_code
    
     # Validate cell phone number (only numbers and exactly 9 digits)
    def validate_phone_format(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError('O número de telemóvel deve conter apenas números.')
        if len(phone) != 9:
            raise forms.ValidationError('O número de telemóvel deve conter exatamente 9 dígitos.')
        return phone

    # Validate the NIF(Tax Number) (only numbers and 9 digits)
    def validate_nif_format(self):
        nif = self.cleaned_data.get('nif')
        if nif and not nif.isdigit():
            raise forms.ValidationError('O NIF deve conter apenas números.')
        if len(nif) != 9:
            raise forms.ValidationError('O NIF deve conter exatamente 9 dígitos.')
        return nif