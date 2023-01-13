from django.db import models
from accounts.models import User
from menu.models import FoodItem

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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