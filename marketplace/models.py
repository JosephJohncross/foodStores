from django.db import models
from accounts.models import User
from menu.models import FoodItem

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)    
    quantity =  models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return self.fooditem.food_title

class Tax(models.Model):
    """Model representing tax charged during food item purchase"""

    tax_type = models.CharField(max_length=20, unique=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Tax percentage (%)")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Tax"
    def __str__(self):
        return self.tax_type

