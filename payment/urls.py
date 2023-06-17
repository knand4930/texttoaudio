from django.urls import path
from . import views

urlpatterns =[
    path('subcriptions', views.subscriptions, name='subscriptions'),
    path('pyament/status', views.pyament_status, name='pyament_status'),
]