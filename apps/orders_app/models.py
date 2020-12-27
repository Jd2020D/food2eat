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

#w
def isMealOrdered(meal_id,user_id):
    if len(User.objects.get(id=user_id).orders.last().items.filter(meal_id=meal_id)):
        return True
    return False
def getOrderedMealsIds(user_id):
    return [dictOf['meal_id'] for dictOf in list(User.objects.get(id=user_id).orders.last().items.all().values('meal_id'))]
def createOrder(Inputs):
    pass
def deleteOrder(Inputs):
    pass
def getOrderedById(Inputs):
    pass
def createItem(Inputs,user_id):
    meal=Meal.objects.get(id=int(Inputs['meal_id']))
    OrderedItem.objects.create(quantity=int(Inputs['quantity']),
    order=User.objects.get(id=user_id).orders.last(),meal=meal)

def removeItem(Inputs,user_id):
    order=User.objects.get(id=user_id).orders.last()
    OrderedItem.objects.get(order_id=order.id,meal_id=int(Inputs['meal_id'])).delete()
    
def getTotalCost(user_id):
    totalCost=0
    for cost in [(item.meal.price*item.quantity) for item in getUserOrderedItems(user_id) ]:
        totalCost+=cost
    return totalCost
def getOrderedItemsQuantities(user_id):
    dicts= User.objects.get(id=user_id).orders.last().items.values('meal_id','quantity')
    idToquantityDict={}
    for dict in dicts:
        idToquantityDict[dict['meal_id']]=dict['quantity']
    return idToquantityDict

def changeOrderedItemQuantity(meal_id,user_id,quantity):
    order=User.objects.get(id=user_id).orders.last()
    item=OrderedItem.objects.get(order_id=order.id,meal_id=meal_id)
    item.quantity=int(quantity)
    item.save()
    total_cost=getTotalCost(user_id)
    return {'id':item.id,'item_cost':item.meal.price*item.quantity,'total_cost':total_cost}


def getUserOrderedItems(user_id):
    return User.objects.get(id=user_id).orders.last().items.all()


def CreateNewOrder(user_id):
    Order.objects.create(user=User.objects.get(id=user_id))

def getOrdersHistory(user_id):
    orders=User.objects.get(id=user_id).orders.all()
    history={}
    for i in range(len(orders)-1):
        history[orders[i].id]=orders[i+1].created_at
    return history

def getAllOrders(user_id):
    return User.objects.get(id=user_id).orders.all()

def getOrderId(user_id):
    user = User.objects.get(id=user_id)
    return user.orders.last().id