from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from accounts.forms import UserProfileForm
from accounts.views import check_role_vendor
from .forms import VendorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import UserProfile
from .models import Vendor
from .utils import get_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify

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
        "form": category_form   
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
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category added successfully")
            return redirect('menu_builder')
        else:
            messages.warning(request, form.errors.as_data().get('category_name')[0])
            return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
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
            'category': category
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
        }

        return render(request, 'vendor/edit_food_item.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, category_id, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    food_item.delete()

    messages.success(request, "Food item deleted successfully")
    return redirect('fooditems_by_category', category_id)
