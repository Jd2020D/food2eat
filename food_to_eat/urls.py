from django.urls import path ,include

urlpatterns = [
    path('', include('apps.users_app.urls')),
    path('meals/', include('apps.orders_app.urls')),
    path('partner/', include('apps.restaurants_app.urls')),

]