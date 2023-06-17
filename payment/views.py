from django.shortcuts import render, redirect
from django.conf import settings
# from stripe.api_resources import charge
import razorpay
from main.models import *
from .models import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.

def subscriptiontype(request):
    obj = SubscriptionType.objects.all()
    return render(request, 'subscription.html', {'obj': obj})

def subscriptions(request):
    if(request.user.is_authenticated is False):
        return redirect("signin")
    obj = SubscriptionType.objects.all()
    if request.method == 'POST':
        plan = request.POST.get('plan')         
        name = request.POST.get('name')
        plandata = plan[1:]
        planvalues = float(plandata)
        user= request.user
        amount = int(planvalues) *100
        
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET),
        )
        
        response_payment = client.order.create(dict(
            amount=amount,
            currency = "INR",
        ))

        order_id = response_payment['id']
        order_status = response_payment['status']

        
        if order_status == 'created':   
            data = Profile(
                user = user,
                name = name,
                amount =amount,
                order_id = order_id,
            )
            data.save()
            
            response_payment['name'] = name
            return render(request, 'subscription.html', {'payment':response_payment})   

    return render(request, 'subscription.html', {'obj': obj})



def pyament_status(request):
    if(request.user.is_authenticated is False):
        return redirect("signin")
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET),
        )

    try:
        status = client.utility.verify_payment_signature(params_dict)
        paystatus = Profile.objects.get(order_id=response['razorpay_order_id'])        
        paystatus.razorpay_payment_id = response['razorpay_payment_id']
        paystatus.paid = True
        paystatus.is_verified = True
        paystatus.auth_token = Profile.auth_token
        paystatus.email = request.user.email
        
        if paystatus.amount == 16000:
            paystatus.subscription_type = "transcribe"
            expiry = datetime.now() + timedelta(days=30) 
            paystatus.pro_expire_date = expiry
        
        if paystatus.amount == 90000:
            paystatus.subscription_type = "transcribe"
            expiry = datetime.now() + timedelta(days=180) 
            paystatus.pro_expire_date = expiry

        if paystatus.amount == 170000:
            paystatus.subscription_type = "transcribe"
            expiry = datetime.now() + timedelta(days=360) 
            paystatus.pro_expire_date = expiry
        
        paystatus.save()
        
        msg_plain = render_to_string("email.txt")
        msg_html = render_to_string("email.html")
        send_mail("Your Payment Has Been Successfully Received", msg_plain, settings.EMAIL_HOST_USER, [request.user.email], html_message= msg_html)
        
        return redirect('adminpanel')
    except:
        return render(request, 'pyament_status.html', {'status': False})
    
    # return render(request, 'pyament_status.html')
#https://github.com/CodeShika/coffee_full_project/blob/main/django_razorpay

