from django.contrib import admin
from .models import Cart, CartItem, Tax
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'modified_at')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('fooditem', 'quantity')

class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')
    
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Tax, TaxAdmin)