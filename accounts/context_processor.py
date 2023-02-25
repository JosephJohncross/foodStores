from django.conf import settings
from vendor.models import Vendor

# def get_vendor(request):
#     try:
#         vendor = Vendor.objects.get(user=request.user)
#         print(vendor + "account context")
#     except Exception as e:
#         print(f"{e}  account context")
#         vendor = Vendor.objects.none()
#     return dict(vendor=vendor)

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}

def get_forward_coding_api(request):
    return { "FORWARD_GEOCODING": settings.FORWARD_GEOCODING }

def get_paystack_key(request):
    return {'PAYSTACK_KEY': settings.PAY_STACK_KEY }

# Returns user role 
def get_user_role(request):
    role = "anon"
    if request.user.is_authenticated:
        if request.user.role == 1:
            role="vendor"
        elif request.user.role == 2:
            role = "customer"
        else:
            role = "anon"
    return  {'role': role}