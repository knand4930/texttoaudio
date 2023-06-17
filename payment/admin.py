from django.contrib import admin
from .models import *
# Register your models here.

class SubscriptionAdmin(admin.ModelAdmin):
    list_display= ('name', 'create_at', 'balance')
    list_filter= ('name', 'create_at', 'balance')
admin.site.register(SubscriptionType, SubscriptionAdmin)


class SelectServiceAdmin(admin.ModelAdmin):
    list_display= ('name', 'create_at')
    list_filter= ('name', 'create_at')
admin.site.register(SelectService, SelectServiceAdmin)

class FrontPageSubscriptionAdmin(admin.ModelAdmin):
    list_display= ('subscription', 'planname', 'urlname', 'planstatus', 'create_at')
admin.site.register(FrontPageSubscription, FrontPageSubscriptionAdmin)