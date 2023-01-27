from django.shortcuts import render
from vendor.models import Vendor

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D

def home(request):
    location_active = False    
    if 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        pnt = GEOSGeometry(f'POINT({lng} {lat})')

        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=2000))).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")

        for v in vendors:
            v.kms = round(v.distance.km)
            print(f'{v.kms} test location')
        location_active = True
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:3]
    context = {
        'vendors': vendors,
        'location_active': location_active
    }
    return render(request, 'home.html', context)