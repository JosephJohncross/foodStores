from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.forms import UserFormInfo, UserProfileForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from accounts.models import UserProfile
from orders.models import Order

@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_info_form = UserFormInfo(request.POST, instance=request.user)
        user_profile = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_info_form.is_valid() and user_profile.is_valid():
            user_info_form.save()
            user_profile.save()
            messages.success(request, 'User profile updated successfully')
            return redirect('cprofile')
        else:
            print(user_info_form.errors, user_profile.errors)
    else:
        user_info_form = UserFormInfo(instance=request.user)
        user_profile = UserProfileForm(instance=profile)
    
    context = {
        'user_info_form' : user_info_form,
        'user_profile': user_profile,
        'profile': profile
    }
    return render(request, 'customer/cprofile.html', context)

@login_required(login_url='login') 
def c_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered =True).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'customer/c_orders.html', context)