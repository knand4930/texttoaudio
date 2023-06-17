from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.core.mail import message, send_mail
from .helpers import *  
from django.core.paginator import Paginator
from payment.models import *
from datetime import datetime, timedelta
# Create your views here.

def home(request):
    feed = Feedback.objects.all()
    # blog = Blogs.objects.all().order_by(-10)
    return render(request, 'front/homemaster.html')

def adminpanel(request):
    # category = Cat.objects.all()
    obj = FrontPageSubscription.objects.all()

    # try:
    #     if request.user.is_authenticated:
    #         profile_pro = Profile.objects.filter(user=request.user).last()
    #         request.session['profile_pro'] = profile_pro.paid
    #         if profile_pro.paid == True:
    #             subscription_type = profile_pro.subscription_type
    #             print("Subscription type is :- ", subscription_type)         
    #             return render(request, 'back/adminpanel.html', {'subscription_type':subscription_type})

    
    #     return render(request, 'back/adminpanel.html')
    # except Exception as e:
    #     print(e)
    #     return redirect('registrations')
    return render(request, 'back/adminpanel.html', { 'obj':obj})


def feedback(request):
    if(request.user.is_authenticated is False):
        return redirect("signin")
    if request.method == 'POST':
        feed = request.POST.get('feed')
        img = request.FILE.get('img')
        feeds = Feedback()
        feeds.username = request.user
        feeds.feed = feed
        feeds.img = img
        feeds.save()
        messages.success(request, 'Form submission successful')
    return render(request, 'back/feedback.html')


def contactus(request):
    if(request.user.is_authenticated is False):
        return redirect("signin")
    if request.method == 'POST':
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        title = request.POST.get('title')
        msg = request.POST.get('msg')
        contact = ContactUs()
        contact.fname = fname
        contact.email = email
        contact.title = title
        contact.msg = msg
        contact.save()
        messages.success(request, 'Form submission successful')
    return render(request, 'back/contactus.html')


def blogs(request):
    obj = Blogs.objects.all().order_by('-pk')
    paginator = Paginator(obj, 1) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'back/blogs.html', {'obj': obj, 'page_obj': page_obj})

def blogdetails(request, word):
    obj = Blogs.objects.get(slug=word)
    return render(request, 'back/blogdetails.html', {'obj': obj})



def login_attempts(request):
        
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username=username).first()
        
        if user_obj is None:
            messages.error(request, 'User Not Found')
            return redirect('signin')
        
        profile_obj = Profile.objects.filter(user=user_obj).first()
        
        if not profile_obj.is_verified:
            messages.error(request, 'profile is not verified please check your Email Address')
            return redirect('signin')
        
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request, 'Wrong Password')
            return redirect('signin')
        
        login(request, user)
        return redirect('adminpanel')
                
    return render(request, 'front/login.html')


def register_attempts(request):    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'User Name Already Exists')
                return redirect('signup')
            
            if User.objects.filter(email=email).first():
                messages.error(request, 'Email Address already Exists')
                return redirect('signup')
            user_obj = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            
            auth_token=str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('token_send')
        except Exception as e:
            print(e)
        
    return render(request, 'front/registrations.html')


def success(request):
    return render(request, 'front/success.html')

def token_send(request):
    return render(request, 'front/token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            
            if profile_obj.is_verified:
                messages.success(request, 'Your Account has been Alread verified')
                return redirect('signin')
            
            profile_obj.is_verified = True
            profile_obj.amount = 1
            profile_obj.subscription_type = "free"
            profile_obj.order_id = "freetrial"
            profile_obj.razorpay_payment_id= "freetrial"
            expiry = datetime.now() + timedelta(seconds=900)
            profile_obj.pro_expire_date = expiry
            profile_obj.paid = True
            profile_obj.save()          
            messages.success(request, 'Congratulation , Your Account has been verified')
            return redirect('signin')
                
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return render(request, 'front/error.html')


def send_mail_after_registration(email, token):
    subject = "Your Account Has Been Verified"
    message = f"Hello, Paste the link to verify your account http://127.0.0.1:8000/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipients_list = [email]
    send_mail(subject, message, email_from, recipients_list)

#https://github.com/boxabhi/yotube_django_email.git


@csrf_exempt
def logout_view(request):
    if(request.user.is_authenticated is False):
        return redirect("signin")
    logout(request)
    return redirect('signin')

def changepassword(request , token):
    context = {}   
    
    try:
        profile_obj = Profile.objects.filter(auth_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/changepassword/{token}')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/changepassword/{token}')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('signin')                
        
        
    except Exception as e:
        print(e)
    return render(request , 'front/changepassword.html' , context)

#https://github.com/boxabhi/youtube_reset_password_django/blob/master/accounts/views.py


def forgetpassword(request):
    
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('forgetpassword')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.auth_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('forgetpassword')
    
    except Exception as e:
        print(e)
    return render(request , 'front/forgetpasswords.html')
