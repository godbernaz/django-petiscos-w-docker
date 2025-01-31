from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserBilling

CustomUser = get_user_model()

class UserBillingInline(admin.TabularInline):  
    model = UserBilling
    extra = 0  # Para evitar a criação de linhas vazias
    fields = ['name', 'address', 'postal_code', 'city', 'phone', 'nif', 'is_default']
    readonly_fields = ['is_default']  # O campo padrão pode ser gerenciado apenas pelo utilizador

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['username', 'email']
    search_fields = ['username', 'email', 'billing_profiles__city', 'billing_profiles__postal_code', 'billing_profiles__phone']
    list_filter = ['is_superuser', 'is_staff', 'is_active']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    inlines = [UserBillingInline]  # Adicionamos os perfis de faturação como um dropdown

admin.site.register(CustomUser, CustomUserAdmin)