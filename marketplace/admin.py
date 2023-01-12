from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'modified_at')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('fooditem', 'quantity')
    
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
