from django.urls import path     
from . import views
urlpatterns = [
    path('', views.mealsPage),
    path('add_to_cart',views.addMealToCart,name='addToCart')


]