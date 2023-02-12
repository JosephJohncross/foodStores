# from base64 import urlsafe_b64decode
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from  accounts.tokens import account_activation_token
from food_stores import settings
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
    
