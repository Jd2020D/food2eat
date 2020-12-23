from django.urls import path     
from . import views
app_name='users_app'
urlpatterns = [
    path('', views.root),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('myaccount',views.editAccountPage),
    path('update',views.updateAccount)




]