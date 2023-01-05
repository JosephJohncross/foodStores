from django.urls import path, include
from . import views

urlpatterns = [
    path('marketplace', views.marketplace, name="marketplace")
]