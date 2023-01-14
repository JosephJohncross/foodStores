from django.shortcuts import render
from vendor.models import Vendor

def home(request):
    print("testing home url") #checked
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:4]
    print(vendors) #check
    context = {
        'vendors': vendors
    }
    print(context) #checked
    return render(request, 'home.html', context)