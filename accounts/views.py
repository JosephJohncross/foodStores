# from django.http import HttpResponse
import json
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from accounts.models import User, UserProfile
from accounts.utils import detectUser, get_orders_for_6_days, get_revenue_by_months, return_today_orders, send_verification_email
from menu.models import Category, FoodItem
from orders.models import Order
from vendor.forms import VendorForm
from vendor.utils import get_vendor
from .forms import UserForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from vendor.models import Vendor

from django.core.exceptions import  PermissionDenied
from .tokens import account_activation_token
from django.template.defaultfilters import slugify

# Create your views here.

# Restrict the vendor from accessing the cusomer page.
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict the customer from accesing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

# global message setter
message_state = ''

def registerUser(request):
    global message_state

    if request.user.is_authenticated:
        messages.warning(request, "Already logged in")
        message_state = "warning"
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()

            #Send verification email
            mail_subject = "Please acivate your account"
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, "Your account has been registered successfully")
            message_state = 'success'
            return redirect('login')
        else:
            pass
    else:
        form = UserForm() 
    context = {
        'form': form,
        'message_state': message_state
    }
    return render(request, 'accounts/registerUser.html', context)

def activate(request, uidb64, token):
    global message_state
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation! Your account is activated.")
        message_state = 'success'
        return redirect('myAccount')
    else:
        messages.error(request, "Invalid activation link")
        message_state = 'error'
        return redirect('myAccount')

def registerVendor(request):
    global message_state
    if request.user.is_authenticated:
        messages.warning(request, "Already logged in")
        message_state = "warning"
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit = False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor_name =  v_form.cleaned_data['vendor_name']
            vendor.user = user
            vendor.vendor_slug = slugify(vendor_name) + '-' + str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            #Send verification email
            mail_subject = "Please activate your account"
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            
            messages.success(request, "Your account has been registered successfully! Please wait for the approval")
            message_state = 'success'
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
        "message_state": message_state
    }
    return render(request, 'accounts/registerVendor.html', context)

@csrf_protect
def login(request):
    global message_state

    if request.user.is_authenticated:
        messages.warning(request, "Already logged in")
        message_state = "warning"
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful")
            message_state = 'success'
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid login details")
            message_state = 'error'
            return redirect('login')
    context = {
        'message_state': message_state
    }
    return render(request, "accounts/login.html", context)
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logout successful')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    category =  Category.objects.filter(vendor=vendor)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')
    orders_today  = return_today_orders(orders)
    recent_orders = orders[:5]
    
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']

    # Returns number of all food items for a vendor
    food_items = FoodItem.objects.filter(vendor=get_vendor(request))

    context = {
        'category_count': category.count(),
        'orders': orders,
        'orders_count': orders.count(),
        'orders_today': len(orders_today),
        'recent_orders': recent_orders,
        'total_revenue': round(total_revenue, 4),
        'monthly_revenue': get_revenue_by_months(orders),
        'orders_by_day_count': get_orders_for_6_days(orders),
        'food_items': food_items.count()
    }
    return render(request, 'accounts/vendorDashboard.html', context)

def forgot_password(request):
    global message_state
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = "Reset password"
            email_template = 'accounts/emails/password_reset_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Password reset link has been sent to your email address")
            message_state = 'success'
            return redirect('login')
        else:
            messages.error("Account does not exist")
            message_state = 'error'
            return redirect('forgot_password')
         
    return render(request, "accounts/forgot_password.html")

def reset_password_validate(request, uidb64,  token):
    global message_state
    # Validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, "Please reset your password")
        message_state = 'info'
        return redirect('reset_password')
    else:
        messages.error(request, "This link has expired")
        message_state = 'error'
        return redirect('myAccount')

def reset_password(request):
    global message_state
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            message_state = 'success'
            return redirect('login')
        else:
            messages.error(request, 'password do not match')
            message_state = 'error'
            return redirect('reset_password')
    return render(request, "accounts/reset_password.html")