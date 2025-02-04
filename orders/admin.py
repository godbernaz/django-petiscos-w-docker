from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Permite adicionar itens diretamente no pedido

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'billing_info', 'created_at', 'total_price')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]  # Permite visualizar itens do pedido na mesma página

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'meal', 'quantity', 'price', 'total_price')
    search_fields = ('order__id', 'meal__meal_name')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)