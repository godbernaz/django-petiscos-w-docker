# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserBilling

CustomUser = get_user_model()

class UserBillingInline(admin.StackedInline):  
    model = UserBilling
    extra = 0  
    fields = ['address', 'postal_code', 'city', 'phone', 'nif'] 

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Fields displayed in the main panel
    list_display = ['username', 'email']
    search_fields = ['username', 'email', 'billing_info__city', 'billing_info__postal_code', 'billing_info__phone']
    list_filter = ['is_superuser', 'is_staff', 'is_active']

    # Fields displayed on the user details page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'email'),
        }),
        ('Informações de Faturação', {
            'fields': ('billing_address', 'billing_postal_code', 'billing_city', 'billing_phone', 'billing_nif'),
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields displayed when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # Billing fields as read-only
    readonly_fields = [
        'billing_address', 'billing_postal_code', 'billing_city', 'billing_phone', 'billing_nif'
    ]

    # Methods for displaying UserBilling template fields
    def billing_address(self, obj):
        return obj.billing_info.address if obj.billing_info else '-'

    def billing_postal_code(self, obj):
        return obj.billing_info.postal_code if obj.billing_info else '-'

    def billing_city(self, obj):
        return obj.billing_info.city if obj.billing_info else '-'

    def billing_phone(self, obj):
        return obj.billing_info.phone if obj.billing_info else '-'

    def billing_nif(self, obj):
        return obj.billing_info.nif if obj.billing_info else '-'

    # Add a personalized title
    billing_address.short_description = "Morada"
    billing_postal_code.short_description = "Código Postal"
    billing_city.short_description = "Cidade"
    billing_phone.short_description = "Telemóvel"
    billing_nif.short_description = "NIF"

admin.site.register(CustomUser, CustomUserAdmin)
 
