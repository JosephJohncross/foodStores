import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from orders.forms import OrderForm
from marketplace.context_processor import get_cart_amounts
from orders.models import Order, Payment
from marketplace.models import FoodItem, Cart, CartItem, Tax
from .utils import generate_order_number
from .models import OrderedFood
from accounts.utils import send_notification

@login_required(login_url='login')
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart)

    # Gets all vendor ids to save to many to many field vendor of orders  
    vendors_ids = []
    for i in cart_item:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)
    
    get_task = Tax.objects.filter(is_active=True)
    sub_total = 0
    k = {}
    total_data = {}
    for i in cart_item:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id, vendor_id__in=vendors_ids)
        v_id = fooditem.vendor.id
        if v_id in k:
            sub_total = k[v_id]
            sub_total += (fooditem.price * i.quantity)
            k[v_id] = sub_total
        else:
            sub_total = (fooditem.price * i.quantity)
            k[v_id] = sub_total

        # Calculate the tax data
        tax_dict = {}
        for i in get_task:
                tax_type = i.tax_type
                tax_percentage = i.tax_percentage
                tax_amount = round ((tax_percentage * sub_total )/ 100, 2)
                tax_dict.update({tax_type: {str(tax_percentage): str(tax_amount)}})
        
        # Construct total data
        total_data.update({fooditem.vendor.id: {str(sub_total): tax_dict}})


    total = get_cart_amounts(request)['total']
    total_sales_tax = get_cart_amounts(request)['total_sales_tax']

    if request.method == 'POST':
        order = Order()
        form = OrderForm(request.POST)
        if form.is_valid:
            order.user = request.user
            order.first_name = request.POST['first_name']
            order.last_name = request.POST['last_name']
            order.phone = request.POST['phone']
            order.email = request.POST['email']
            order.address = request.POST['address']
            order.country = request.POST['country']
            order.state = request.POST['state']
            order.city = request.POST['city']
            order.pin_code = request.POST['pin_code']
            order.total = total
            order.total_tax = total_sales_tax
            order.total_data = json.dumps(total_data)
            order.payment_method = request.POST['payment_method']
            order.save() #generate the order number
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_ids)
            order.save()

            context = {
                "order_number" : order.order_number,
                'order': order 
            }
            return render(request,'orders/place_order.html', context)
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')

@login_required(login_url='login')
def payments(request):
    # check if request is Ajax
    if request.headers.get('x-request-with') == 'XMLHttpRequest' and request.method == "POST":
    
        # store payment details in the payment model
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order_number = body["order_number"]
        payment_method = body["payment_method"]
        transaction_id = body["transaction_id"]
        status = body['status']

        order = Order.objects.get(user=request.user, order_number= order_number)
        payment = Payment(user=request.user,transaction_id=transaction_id,payment_method=payment_method,amount=order.total,status=status)
        payment.save()

        # store order model
        order.payment = payment
        order.is_ordered = True
        order.save()

        # move the cart items to other food models
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.quantity * item.fooditem.price
            ordered_food.save()
        
        # send order confirmation email to customer
        email_subject = "Thank you for ordering with us"
        mail_template = "orders/order_confirmation_email.html"
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
        }
        send_notification(email_subject=email_subject,  mail_template=mail_template, context=context)
        
        
        # send order received email to the vendor
        email_subject = "You just received an order"
        mail_template = "orders/new_order_recieved.html"
        to_email = []
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_email:
                to_email.append(i.fooditem.vendor.user.email)
        context = {
            'order': order,
            'to_email': to_email,
        }
        send_notification(email_subject=email_subject,  mail_template=mail_template, context=context)
        # Clear the cart if payment is successful 
        # cart_items.delete()
        
        # return back to ajax with the status success or failure
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id
        }
        return JsonResponse(response)

    return HttpResponse("Payment View")

def order_complete(request):
    order_number =  request.GET.get('order_number')
    transaction_id = request.GET.get('transaction_id')

    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.fooditem.price * item.quantity)
        total_tax = order.total_tax
        total = order.total 
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal':subtotal,
            'total_tax': total_tax,
            'total': total

        }
        return render(request, 'orders/order_complete.html', context)
    except Exception as e:
        print(e)
        return redirect('myAccount')