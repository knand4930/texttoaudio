from django.urls import path
from . import views
# from .views import Registrations, LoginView
urlpatterns = [
    # path('', views.home, name='home'),
    path('home-pages', views.adminpanel, name='adminpanel'),
    path('feedback', views.feedback, name='feedback'),
    path('contactus', views.contactus, name='contactus'),
    path('blogs', views.blogs, name='blogs'),
    path('blogdetails/<word>', views.blogdetails, name='blogdetails'),
    path('signin', views.login_attempts, name='signin'),
    path('signup', views.register_attempts, name='registrations'),
    path('token_send', views.token_send, name='token_send'),
    path('success', views.success, name='success'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('error', views.error_page, name='error'),    
    path('logout_view', views.logout_view, name='logout_view'),
    path('changepassword/<token>', views.changepassword, name='changepassword'),
    path('forgetpassword', views.forgetpassword, name='forgetpassword'),
    
    
    # path('registrations', Registrations.as_view(), name='registrations'),
    # path('forgetpassword', views.forgetpasswords, name='forgetpassword'),
    # path('signin', LoginView.as_view(), name='signin'),
]
