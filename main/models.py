from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from datetime import datetime, timedelta, date
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.
import datetime
from datetime import timedelta
from datetime import datetime as dt

today = datetime.date.today()

class Profile(models.Model):
    STATUS_CHOICES=(
        ('marketing', "MARKETING"),
        ('book', "BOOK"),
        ('transcribe', 'TRANSCRIBE'),
        ('book_marketing', "BOOKS & MARKETING"),
        ('book_transcribe', "BOOKS & TRANSCRIBE"),
        ('marketing_transcribe', "MARKETING & TRANSCRIBE"),
        ('all', 'ALL PACKAGES')
    )    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=1000)
    amount = models.IntegerField(default=0)
    order_id = models.CharField(max_length=500)
    razorpay_payment_id = models.CharField(max_length=500)
    paid = models.BooleanField(default=False)
    pro_expire_date = models.DateField(null=True, blank=True)
    subscription_type = models.CharField(max_length=100,choices=STATUS_CHOICES, default='free')
    create_at = models.DateTimeField(auto_now_add=True)
    

@receiver(pre_save, sender=Profile)
def update_active(sender, instance, *args, **kwargs):
    if instance.pro_expire_date == today:
        instance.paid = False
    else:
        instance.paid = True
        
        
        
    def __str__(self):
        return self.user.username


class Feedback(models.Model):
    username = models.CharField(max_length=100, default=None)
    feed = models.TextField()
    img = models.ImageField(upload_to="feedback/")
    create_at = models.DateTimeField(auto_now_add=True)
    
class ContactUs(models.Model):
    STATUS=(
        ('NEW', 'new'),
        ('OPEN', 'open'),
        ('CLOSED', 'closed'),
        ('REPLY', 'reply'),
        ('FAKES', 'fakes'),
    )
    
    fname = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    title = models.CharField(max_length=250)    
    msg = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='NEW')
    create_at = models.DateTimeField(auto_now_add=True)
    
class Blogs(models.Model):


    title = models.CharField(max_length=250)
    img = models.ImageField(upload_to='blog/images/')
    slug = models.SlugField(max_length=250)
    short = models.TextField()
    txt = RichTextField()
    create_at = models.DateTimeField(auto_now_add=True)
    
    
    def save(self):
        if not self.id:
            self.slug = slugify(self.title)

        super(Blogs, self).save()
