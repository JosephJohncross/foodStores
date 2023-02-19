from django.contrib import admin
from .models import OrderedFood, Payment, Order

class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields= ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = [ "order_number", "user", "status", "payment_method", 'order_placed_to', "is_ordered"]
    inlines = [OrderedFoodInline]


admin.site.register(OrderedFood)
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)


