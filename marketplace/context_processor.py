from .models import Cart

# Gets the number of items added to cart by a user
def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.filter(user=request.user)
            if cart_item:
                cart_count = cart_item.count()
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)

