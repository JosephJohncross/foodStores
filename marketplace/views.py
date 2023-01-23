from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.db.models import Prefetch 
from django.shortcuts import get_object_or_404
from menu.models import Category, FoodItem
from vendor.models import Vendor
from .models import Cart, CartItem
from .context_processor import get_cart_counter
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True).order_by('vendor_name').values()
    vendors_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendors_count': vendors_count
    }
    return render(request, 'marketplace/listing.html', context)

def vendor_details(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    context = {
        'vendor': vendor
    }
    return render(request, 'marketplace/vendor_details.html', context)

def vendor_menu(request, vendor_slug):
    slug = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )

    context = {
        'vendor_slug': slug,
        'vendor': vendor,
        'categories': categories
    }
    return render(request, 'marketplace/vendor_menu.html', context)

def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-request-with') == 'XMLHttpRequest':
            # Checksif food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if the user has added food item to cart
                try:
                    checkCart = Cart.objects.get(user=request.user)
                    try:
                        checkCartItem = CartItem.objects.get(cart = checkCart, fooditem = fooditem)
                        # Increase cart quantity
                        checkCartItem.quantity += 1
                        checkCartItem.save()
                        return JsonResponse({"status": "Success", "message": "Increased the cart quantity", "cartcounter": get_cart_counter(request)})
                    except:
                        checkCartItem = CartItem.objects.create(cart = checkCart, fooditem = fooditem, quantity= 1)
                        return JsonResponse({'status': 'Success', "message": "Item added to cart", "cartcounter": get_cart_counter(request)})
                except Exception as e:
                    # Add item to cart for the first time
                    checkCart = Cart.objects.create(user=request.user)
                    checkCartItem = CartItem.objects.create(cart = checkCart, fooditem = fooditem, quantity=1)
                    return JsonResponse({"status": "Success", "message": "Item added to cart", "cartcounter": get_cart_counter(request)})
            except:
                return JsonResponse({"status": "Failed", "message": "This food does not exist"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    return JsonResponse({"status": "Failed", "message": "Please login to continue"})

@login_required(login_url='login')
def decrement_cartitem(request, cartitem_id=None):
    cart_item = get_object_or_404(CartItem, pk=cartitem_id)

    if request.user.is_authenticated:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return JsonResponse({"status": "Success", "message": "Cart item decremented"})
        else:
            return JsonResponse({"status": "Failed", "message": "Item is at the minimum"})
    return JsonResponse({"status": "Failed", "message": "Please login to continue"})

@login_required(login_url='login')
def increment_cartitem(request, cartitem_id=None):
    cart_item = get_object_or_404(CartItem, pk=cartitem_id)

    if request.user.is_authenticated:
        if request.headers.get('x-request-with') == 'XMLHttpRequest':

            if cart_item.quantity >= 1:
                cart_item.quantity += 1
                cart_item.save()
                return JsonResponse({"status": "Success", "message": "Cart item incremented"})
            else:
                return JsonResponse({"status": "Success", "message": "Item is at the minimum"})
        return JsonResponse({"status": "Failed", "message": "Invalid request"})
    return JsonResponse({"status": "Failed", "message": "Please login to continue"})

@login_required(login_url='login')
def delete_cartitem(request, cartitem_id=None):

    if request.user.is_authenticated:
        if request.headers.get('x-request-with') == 'XMLHttpRequest':
            try:
                cart_item = get_object_or_404(CartItem, pk=cartitem_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({"status": "Success", "message": "Item deleted successfully from cart"})
                else:
                    return JsonResponse({"status": "Failed", "message": "Item no longer in cart"})
            except:
                return JsonResponse({"status": "Failed", "message": "Item no longer in cart"})
        return JsonResponse({"status": "Failed", "message": "Invalid request"})
    return JsonResponse({"status": "Failed", "message": "Please login to continue"})


def search(request):
    address = request.GET["restaurant_name"]
    latitude = request.GET["lat"]
    longitude = request.GET["lng"]
    search_keyword = request.GET["restaurant_name"]

    # returns vendor id's that has the food items the user is looking for 
    food_item_by_vendor = FoodItem.objects.filter(food_title__icontains=search_keyword, is_available=True).values_list('vendor', flat=True)

    vendor = Vendor.objects.filter(Q(id__in=food_item_by_vendor) | Q(vendor_name__icontains=search_keyword, is_approved=True, user__is_active=True))
    vendor_count = vendor.count()
    context = {
        "vendors" : vendor,
        "vendors_count": vendor_count
    }
    return render(request, 'marketplace/listing.html', context)
    # return HttpResponse("Search page")