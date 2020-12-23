from django.urls import path     
from . import views
app_name='users_app'
urlpatterns = [
    path('', views.root),
    path('signin',views.viewSignInPage),
    path('signup',views.viewSignUpPage),
    path('signup/partner',views.viewSignUpPartnerPage),
    path('contact_us',views.contactResult),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('myaccount',views.editAccountPage),
    path('update',views.updateAccount),
    path('about_us',views.viewAboutUs)
]
