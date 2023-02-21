# from base64 import urlsafe_b64decode
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from  accounts.tokens import account_activation_token
from food_stores import settings
from datetime import timezone, datetime
# from gmail import sendingMessage

def detectUser(user):
    redirectUrl = ""
    if user.role == 1:
        redirectUrl = "vendorDashboard"
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "customerDashboard"
        return redirectUrl
    elif user.role is None and user.is_superadmin:
        redirectUrl = "/admin"
        return redirectUrl

def return_today_orders(orders):
    orders_for_today = []
    now = datetime.now()
    # today = datetime.time(now.hour, now.minute, now.second, now.microsecond)
    today = datetime(now.year, now.month, now.day, 0, 0, 0, 0, tzinfo=None)
    for order in orders:
        order_date = datetime(order.created_at.year, order.created_at.month, order.created_at.day, order.created_at.hour, order.created_at.minute, order.created_at.second, order.created_at.microsecond, tzinfo=None)
        if order_date > today:
            orders_for_today.append(order)
    return orders_for_today

# Returns revenue per moment
def get_revenue_by_months(orders):
    
    jan=feb=mar=apr=may=jun=jul=aug=sep=ocbe=nov=dec=0
    for order in orders:
        order_date = datetime(order.created_at.year, order.created_at.month, order.created_at.day)
        if (order_date.month == 1):
            jan += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 2):
            feb += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 3):
            mar += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 4):
            apr += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 5):
            may += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 6):
            jun += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 7):
            jul += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 8):
            aug += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 9):
            sep += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 10):
            ocbe += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 11):
            nov += order.get_total_by_vendor()['grand_total']
        elif (order_date.month == 12):
            dec += order.get_total_by_vendor()['grand_total']


    context = {
        "Jan": jan,
        "Feb": feb,
        "Mar": mar,
        "Apr": apr,
        "May": may,
        "Jun": jun,
        "Jul": jul,
        "Aug": aug,
        "Sep": sep,
        "Oct": ocbe,
        "Nov": nov,
        "Dec": dec,
    }
    return context

# Returns number of orders for 6 indivdual days
def get_orders_for_6_days(orders):
    recent_orders_6 = {}

    now = datetime.now()
    today = datetime(now.year, now.month, now.day)

    today_day = today.day
    
    for i in range(0,6):
        string_formated_day = ''
        order_count = 0
        for order in orders:
            order_date = datetime(order.created_at.year, order.created_at.month, order.created_at.day)
            string_formated_day = order_date.strftime("%b")
            if order_date.day == today_day:
                order_count += 1
        recent_orders_6.update({f'{string_formated_day} {today_day}' : order_count})
        today_day -= 1

    print(recent_orders_6)
    return recent_orders_6


def send_verification_email(request, user, mail_subject, email_template):
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    # sendingMessage(user.email, mail_subject, message)
    mail.send()

def send_notification(email_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL or "josephibochi2@gmail.com"
    message = render_to_string(mail_template, context)
    if (isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(email_subject, message, from_email, to=to_email)
    mail.send()
    
