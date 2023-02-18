from django.urls import path
from accounts import views as CustomerView
from . import views

urlpatterns = [
    path('', CustomerView.customerDashboard, name="customer"),
    path('profile/', views.cprofile, name="cprofile"),
    path('c_orders/', views.c_orders, name="c_orders"),
]