from django.urls import path, include
from . import views

urlpatterns = [
    path('marketplace', views.marketplace, name="marketplace"),
    path('<slug:vendor_slug>/', views.vendor_details, name='vendor_details'),
    path('<slug:vendor_slug>/menu/', views.vendor_menu, name="vendor_menu"),

    # cart
    path('add_to_cart/<int:food_id>', views.add_to_cart, name='add_to_cart'),
    path('decrement_cartitem/<int:food_id>', views.decrement_cartitem, name='decrement_cartitem'),
    path('increment_cartitem/<int:food_id>', views.increment_cartitem, name='increment_cartitem'),
]