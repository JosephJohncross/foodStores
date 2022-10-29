from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts.models import User, UserProfile
from accounts.utils import detectUser, send_verification_email
from vendor.forms import VendorForm
from .forms import UserForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import  PermissionDenied

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
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()

            #Send verification email
            send_verification_email(request, user)

            messages.success(request, "Your account has been registered successfully")
            message_state = 'success'
            return redirect('registerUser')
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
    # Activate the user by setting the is_active status to True
    return

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
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            #Send verification email
            send_verification_email(request, user)
            
            messages.success(request, "Your account has been registered successfully! Please wait for the approval")
            message_state = 'success'
            return redirect('registerVendor')
        else:
            print('invalid form')
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
    return render(request, 'accounts/vendorDashboard.html')