from djmoney.models.fields import MoneyField
from django.db import models

# https://pythonrepo.com/repo/django-money-django-money-python-django-utilities
class SubscriptionType(models.Model):
    STATUS_CHOICES=(
        ('transcribe', 'TRANSCRIBE'),
    ) 
    name = models.CharField(max_length=100, choices=STATUS_CHOICES)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    create_at = models.DateTimeField(auto_now_add=True)


class SelectService(models.Model):
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FrontPageSubscription(models.Model):
    subscription = models.CharField(max_length=100, default="150, 299, 99")
    planname = models.CharField(max_length=100, default="ranscribe")
    planstatus = models.CharField(max_length=100, default="Basic Plan")
    selectservice = models.ManyToManyField(SelectService)
    urlfileds = models.SlugField(max_length=200)
    urlname = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subscription + ' ' + self.planname






