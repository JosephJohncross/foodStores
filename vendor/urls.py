from django.urls import path
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendorDashboard, name="vendor"),
    path('profile', views.vprofile, name='vprofile'),
    path('menu_builder', views.menu_builder, name='menu_builder'),
    path('menu_builder/category/<int:pk>/', views.fooditems_by_category, name="fooditems_by_category"),

    # food category CRUD
    path('menu_builder/category/add_category', views.add_category, name="add_category"),
    path('menu_builder/category/edit/<int:pk>/', views.edit_category, name="edit_category"),
    path('menu_builder/category/delete/<int:pk>/', views.delete_category, name="delete_category"),

    # food item CRUD
    path('menu_builder/food/add/<int:pk>/', views.add_food, name='add_food'),
    path('menu_builder/food/edit/<int:category_id>/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu_builder/food/delete/<int:category_id>/<int:pk>/', views.delete_food, name='delete_food'),

    #opening hours
    path('opening_hours', views.opening_hours, name="opening_hours"),
    path('opening_hours/add/', views.add_opening_hours, name="add_opening_hours"),
    path('opening_hours/delete/<int:pk>', views.delete_opening_hours, name="delete_opening_hours"),

    #order details for vendor
    path('order_details/<int:order_number>', views.order_details, name="order_details"),
    path('all_orders', views.all_orders, name="all_orders")
]