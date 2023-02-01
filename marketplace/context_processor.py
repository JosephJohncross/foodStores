from accounts.views import check_role_customer
from .models import Cart, CartItem, Tax
from django.contrib.auth.decorators import login_required, user_passes_test

# Gets the number of items added to cart by a user
# @login_required(login_url='login')
# @user_passes_test(check_role_customer)
def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.filter(cart_id=cart)
            for items in cart_item:
                cart_count += 1
        except Exception as e:
            cart_count = 0
    return dict(cart_count=cart_count)
        

# @login_required(login_url='login')
# @user_passes_test(check_role_customer)
def get_items_in_cart(request):
    cart_item = dict()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart_id=cart).order_by('created_at')
            cart_item = dict(cart_item=cart_items)
        except:
            cart_item="No item exist in the cart"
    return dict(cart_item=cart_item)

# @login_required(login_url='login')
# @user_passes_test(check_role_customer)
def get_cart_amounts(request):
    subtotal = 0
    discount_sales = 0
    total_sales_tax = 0
    total = 0

    tax_dict = {}
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            for items in cart_items:
                subtotal += items.quantity  * items.fooditem.price

            get_task = Tax.objects.filter(is_active=True)

            for i in get_task:
                tax_type = i.tax_type
                tax_percentage = i.tax_percentage
                tax_amount = round ((tax_percentage * subtotal )/ 100, 2)
                tax_dict.update({tax_type: {tax_percentage: tax_amount}})

            for key in tax_dict.values():
                for x in key.values():
                    total_sales_tax = x

            total_sales_tax = sum(x for key in tax_dict.values() for x in key.values())
            total = subtotal - discount_sales + total_sales_tax
        except:
            dict(subtotal=subtotal, discount_sales=discount_sales, total_sales_tax=total_sales_tax, total=total) 
    return dict(subtotal=subtotal, discount_sales=discount_sales, total_sales_tax=total_sales_tax, total=total, tax_dict=tax_dict) 
    