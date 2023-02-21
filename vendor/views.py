from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from accounts.forms import UserProfileForm
from django.http.response import HttpResponse, JsonResponse
from accounts.views import check_role_vendor
from orders.models import Order, OrderedFood
from .forms import VendorForm, OpeningHourForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import UserProfile
from .models import Vendor, OpeningHour
from .utils import get_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify
import json
from django.db import IntegrityError
# global message setter
message_state = ''

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    global message_state

    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        try:
            if profile_form.is_valid() and vendor_form.is_valid():
                profile_form.save()
                vendor_form.save()
                messages.success(request, "Profile update successful")
            else:
                print(profile_form.errors.as_json())
        except Exception as e:
            print(e)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor
    }
    return render(request, 'vendor/vprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)

    category_form = CategoryForm()

    context = {
        'categories': categories,
        "form": category_form,
        "vendor": vendor 
    }
    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    global message_state

    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FoodItem.objects.filter( vendor=vendor, category=category)

    food_form = FoodItemForm()

    context = {
        "food_items": food_items,
        "category": category,
        'form' : food_form,
        'vendor': vendor,
    }
    
    return render(request, 'vendor/fooditems_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    global message_state

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save()
            category.slug = slugify(category_name) + '-' + str(category.id)
            category.save() 
            messages.success(request, "Category added successfully")
            return redirect('menu_builder')
        else:
            messages.warning(request, form.errors.as_data().get('category_name')[0])
            return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category updated successfully")
            return redirect('menu_builder')
        else:
            messages.warning(request, form.errors)
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)
        context = {
            'form': form,
            'category': category,
            'vendor': vendor
        }
        return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()

    messages.success(request, "Category deleted successfully")
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request, pk=None):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        category = get_object_or_404(Category, pk=pk)

        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            food.slug = slugify(food_title)
            food.vendor = get_vendor(request)
            food.category = category
            form.save()
            messages.success(request, f"Food added successfully to {food.category} category")
            return redirect('fooditems_by_category', food.category.id)
        else:
            messages.warning(request, form.errors)
            return redirect('menu_builder') 

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, category_id, pk=None):
    vendor = get_vendor(request)
    food_item = get_object_or_404(FoodItem, pk=pk)

    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)

        if form.is_valid():
            food_item = form.save(commit=False)
            food_title = form.cleaned_data['food_title']
            food_item.vendor = get_vendor(request)
            food_item.slug = slugify(food_title)
            form.save()
            messages.success(request, "Food item successfully updated")
            return redirect('fooditems_by_category', category_id)
        else:
            messages.warning(request, form.errors)
            return redirect('fooditems_by_category', category_id)
    else:
        form = FoodItemForm(instance=food_item)
        context = {
            'form': form,
            'category': category_id,
            'food_item': food_item,
            'vendor': vendor
        }

        return render(request, 'vendor/edit_food_item.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, category_id, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    food_item.delete()

    messages.success(request, "Food item deleted successfully")
    return redirect('fooditems_by_category', category_id)

def opening_hours(request):
    opening_hour = OpeningHour.objects.filter(vendor=get_vendor(request))
    vendor = get_vendor(request)
    form = OpeningHourForm()

    context = {
        'form': form,
        'opening_hours': opening_hour,
        "vendor": vendor
    }
    return render(request, 'vendor/openingHour.html', context)


@login_required(login_url='login')
def add_opening_hours(request):
    # Handle the data and save them inside the database
    if request.user.is_authenticated:
        if request.headers.get('x-request-with') == 'XMLHttpRequest' and request.method == "POST":
            data = json.loads(request.body.decode())
            day = data['day']
            from_hour = data['from_hour']
            to_hour = data['to_hour']
            is_closed = data['is_closed']

            try:
                hour = OpeningHour.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        return JsonResponse({'status' : 'Success', "message": "Opening hour added", 'id': hour.id, 'day': day.get_day_display(), "is_closed": "Closed" })
                    else:
                        return JsonResponse({'status' : 'Success', "message": "Opening hour added", 'id': hour.id, 'day': day.get_day_display(), "from_hour": hour.from_hour, "to_hour": hour.to_hour})
            except IntegrityError as e:
                return JsonResponse({'status' : 'Failed', "message": f"{from_hour} - {to_hour} already exist for this day!"})
        else:
            return JsonResponse({'status' : 'Failed', "message": "Error"})

@login_required(login_url='login')
def delete_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-request-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour, pk=pk)
            if hour:
                hour.delete()
                return JsonResponse({'status': 'Success', 'message': 'Hour removed succesfully', 'id': pk})
        else:
            return JsonResponse({'status' : 'Failed', "message": "Error"})

@login_required(login_url='login')
def order_details(request, order_number=None):
    orders = Order.objects.get( order_number=order_number, is_ordered=True)
    ordered_food = OrderedFood.objects.filter(order=orders, fooditem__vendor=get_vendor(request))
    vendor = get_vendor(request)

    context = {
        'order': orders,
        'ordered_food': ordered_food,
        'vendor': vendor,
    } 

    return render(request, 'vendor/order_details.html', context)

# Returns all orders for a particular vendor
@login_required(login_url='login')
def all_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    category =  Category.objects.filter(vendor=vendor)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(request, "vendor/all_orders.html", context)