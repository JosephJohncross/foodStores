from .models import Cart, CartItem
from menu.models import FoodItem

# Gets the number of items added to cart by a user
def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.filter(cart_id=cart)
            for items in cart_item:
                cart_count += 1
        except Exception as e:
            print(e)
            cart_count = 0
    return dict(cart_count=cart_count)

def get_items_in_cart(request):
    cart_item = dict()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart_id=cart).order_by('created_at')
            cart_item = dict(cart_item=cart_items)
        except:
            cart_item="No item exist in the cart"
    print(cart_item)
    return dict(cart_item=cart_item)

def get_cart_amounts(request):
    subtotal = 0
    discount_sales = 0
    total_sales_tax = 0
    total = 0

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        for items in cart_items:
            subtotal += items.quantity  * items.fooditem.price
        total = subtotal - discount_sales + total_sales_tax
        return dict(subtotal=subtotal, discount_sales=discount_sales, total_sales_tax=total_sales_tax, total=total) 