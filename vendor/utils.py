from .models import Vendor

# gets vendor 
def get_vendor(request):
    return Vendor.objects.get(user=request.user)