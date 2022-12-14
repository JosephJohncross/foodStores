from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Prefetch 
from django.shortcuts import get_object_or_404

from menu.models import Category, FoodItem
from vendor.models import Vendor
from .models import Cart
from .context_processor import get_cart_counter


# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
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
                    checkCart = Cart.objects.get(user=request.user, fooditem = fooditem)
                    # Increase cart quantity
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({"status": "Success", "message": "Increased the cart quantity", "cartcounter": get_cart_counter(request)})
                except Exception as e:
                    # Add item to cart for the first time
                    checkCart = Cart.objects.create(user=request.user, fooditem = fooditem, quantity=1)
                    return JsonResponse({"status": "Success", "message": "Added food item to cart", "cartcounter": get_cart_counter(request)})
            except:
                return JsonResponse({"status": "Failed", "message": "This food does not exist"})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
    return JsonResponse({"status": "Failed", "message": "Please login to continue"})