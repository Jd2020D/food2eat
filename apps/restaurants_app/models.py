from django.db import models
from apps.users_app.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=255)
    iconLink=models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Meal(models.Model):
    title = models.CharField(max_length=255)
    imgLink=models.TextField()
    price=models.DecimalField(decimal_places=2, max_digits=5)
    description=models.TextField()
    category=models.ForeignKey(Category, related_name="meals", on_delete = models.CASCADE)
    restaurant=models.ForeignKey(Restaurant, related_name="meals", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def createRestaurant(name,address,phoneNumber,user_id):
    user=User.objects.get(id=user_id)
    restaurant=Restaurant.objects.create(name=name,address=address,phoneNumber=phoneNumber,user=user)
    return restaurant.id

def getRestaurantById(id):
    try:
        return Restaurant.objects.get(id=id)
    except:
        return False

def checkCat(name):
    try:
        Category.objects.get(name=name)
        return True
    except:
        return False


def createMeal(data,restu_id):
    category=Category.objects.get(name=data['category'])
    restaurant=getRestaurantById(restu_id)
    meal=Meal.objects.create(title=data['title'],imgLink=data['imgLink'],price=data['price'],description=data['description'],category=category,restaurant=restaurant)
    return meal.id