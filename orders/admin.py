from django.contrib import admin
from .models import OrderedFood, Payment, Order

admin.site.register(OrderedFood)
admin.site.register(Payment)
admin.site.register(Order)
