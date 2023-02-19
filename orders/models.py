import json
from django.db import models
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor

request_object = ''
class Payment(models.Model):
    """Class represnting the payment model"""

    PAYMENT_METHOD = (
        ('Paystack', 'Paystack'),
        ('FlutterWave', 'FlutterWave')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id

class Order(models.Model):
    """Model representing the user order and information"""
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendors = models.ManyToManyField(Vendor, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length = 50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    total_tax = models.FloatField()
    total_data = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def order_placed_to(self):
        return ", ". join([str(i) for i in self.vendors.all()])
    
    def get_total_by_vendor(self):
        subtotal = 0
        tax = 0
        tax_dict = {}

        vendor = Vendor.objects.get(user=request_object.user)
        if self.total_data: 
            total_data = json.loads(self.total_data)
            data = total_data.get(str(vendor.id))

            for key,value in data.items():
                subtotal += float(key)
                tax_dict.update(value)

                # Calculate tax
                for i in value:
                    for j in value[i]:
                        tax += float(value[i][j])
        grand_total = float(tax) + float(subtotal)
       
        context = {
            'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,
            'tax_dict': tax_dict
        }
        return context   

    def __str__(self):
        return self.order_number


class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_title