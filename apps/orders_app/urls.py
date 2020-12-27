from django.urls import path     
from . import views
urlpatterns = [
    path('', views.mealsPage),
    path('cart', views.cartPage),
    path('add_to_cart',views.addMealToCart,name='addToCart'),
    path('remove_from_cart',views.removeMealFromCart,name='removeFromCart'),
    path('change_order_quantity/<meal_id>',views.changeOrderQuantity,name='changeOrderQuantity'),
    path('cart/checkout',views.checkOut),
    path('cart/history',views.viewHistory)
    
    ]