from django.db import models
from apps.users_app.models import User
from apps.restaurants_app.models import Restaurant,Meal

class Order(models.Model):
    user=models.ForeignKey(User,related_name="orders", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderedItem(models.Model):
    quantity = models.IntegerField()
    order=models.ForeignKey(Order,related_name="items", on_delete = models.CASCADE)
    meal=models.ForeignKey(Meal,related_name="items", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def createOrder(Inputs):
    pass
def deleteOrder(Inputs):
    pass
def getOrderedById(Inputs):
    pass
