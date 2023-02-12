from django.shortcuts import render, redirect
from django.http import HttpResponse

from orders.forms import OrderForm
from marketplace.context_processor import get_cart_amounts
from orders.models import Order
from .utils import generate_order_number

# Create your views here.
def place_order(request):
    total = get_cart_amounts(request)['total']
    subtotal = get_cart_amounts(request)['subtotal']
    total_sales_tax = get_cart_amounts(request)['total_sales_tax']
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid:
            order = Order()
            print(order_form)
            order.user = request.user
            order.first_name = order_form.cleaned_data['first_name']
            order.last_name = order_form.cleaned_data['last_name']
            order.phone = order_form.cleaned_data['phone']
            order.email = order_form.cleaned_data['email']
            order.address = order_form.cleaned_data['address']
            order.country = order_form.cleaned_data['country']
            order.state = order_form.cleaned_data['state']
            order.city = order_form.cleaned_data['city']
            order.pin_code = order_form.cleaned_data['pin_code']
            order.total = total
            order.total_tax = total_sales_tax
            order.payment_method = request.POST['payment_method']
            order.save() #generate the order number
            order.order_number = generate_order_number(order.id)
            order.save()

            context = {
                "order_number" : order.order_number,
                'order': order 
            }
            return render(request,'orders/place_order.html', context)
        else:
            print(order_form.errors)

    return render(request, 'orders/place_order.html')

def payments(request):
    return HttpResponse("Payment View")