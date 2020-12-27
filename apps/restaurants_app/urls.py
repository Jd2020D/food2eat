from django.urls import path     
from . import views
urlpatterns = [
    path('', views.partnerPage),
    path('remove_meal_from_partner',views.removeMealFromPartner),
    path('addMeal',views.addMeal),
    path('editMeal',views.editMeal),
    path('updateMeal',views.updateMeal)

]
#comment



