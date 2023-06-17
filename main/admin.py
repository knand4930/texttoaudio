from django.contrib import admin
from django.contrib.auth.models import Permission
# Register your models here.
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'name', 'email' ,'amount', 'pro_expire_date','subscription_type', 'paid','create_at')
    list_filter = ('user', 'user', 'amount', 'pro_expire_date','create_at')
    # readonly_fields = ('user', 'auth_token', 'is_verified', 'create_at', 'name', 'email' ,'amount', 'pro_expire_date','subscription_type','razorpay_payment_id','order_id', 'paid')

admin.site.register(Profile, ProfileAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('username', 'create_at')
    readonly_fields = ('username', 'create_at')
    list_filter = ('username', 'create_at')
    
admin.site.register(Feedback, FeedbackAdmin)



class ContactUskAdmin(admin.ModelAdmin):
    list_display = ('email', 'create_at', 'status')
    readonly_fields = ('email', 'create_at', 'fname', 'title', 'msg')
    list_filter = ('email', 'create_at')
    
admin.site.register(ContactUs, ContactUskAdmin)


class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at')
    list_filter = ('create_at',)
    prepopulated_fields ={'slug': ('title',)}
    
admin.site.register(Blogs, BlogsAdmin)