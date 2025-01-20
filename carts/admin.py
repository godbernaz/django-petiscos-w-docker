# carts/admin.py
from django.contrib import admin
from .models import Cart, CartItem

# Itens do Carrinho Inline
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Permite adicionar novos itens diretamente no painel do carrinho
    fields = ('meal', 'quantity', 'total_price',)  # Adiciona 'total_price' à lista de campos
    readonly_fields = ('total_price',)  # Marca 'total_price' como somente leitura, já que é calculado automaticamente

# Carrinho de Compras Admin
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]  # Exibe os itens do carrinho dentro do painel do carrinho
    list_display = ('user', 'created_at', 'total_cart_price')  # Exibe o utilizador, a data de criação do carrinho e o preço total do carrinho

    def total_cart_price(self, obj):
        return obj.total_cart_price  # Adiciona a propriedade total_cart_price ao admin
    total_cart_price.short_description = 'Total Price'  # Altera a descrição do cabeçalho da coluna

admin.site.register(Cart, CartAdmin)