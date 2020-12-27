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
    return {'id':restaurant.id,'name':restaurant.name}

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
    meal=Meal.objects.create(title=data['title'],imgLink=data['imgLink'],price=float(data['price']),description=data['description'],category=category,restaurant=restaurant)
    return meal

def userHasResturant(user_id):
    try:
        res=Restaurant.objects.get(user_id=user_id)
        return {'id':res.id,'name':res.name}
    except:
        return False
def getRestaurantMealsById(restaurant_id):
    return Restaurant.objects.get(id=restaurant_id).meals.all()

def getCategories():
    print(Category.objects.all())
    print('wwwwwwwwwwwwwwwwww')
    return Category.objects.all()

def getMealById(meal_id,partner_id):
    try:
        meal=Meal.objects.get(id=int(meal_id),restaurant_id=partner_id)
        return meal
    except:
        return False

def removeMealFromPartner(meal_id,partner_id):
        meal=Meal.objects.get(id=meal_id,restaurant_id=partner_id)
        meal.delete()
def updateMeal(Inputs):
    meal=Meal.objects.get(id=int(Inputs['meal_id']))
    meal.title=Inputs['title']
    meal.description=Inputs['description']
    meal.imgLink=Inputs['imgLink']
    meal.price=float(Inputs['price'])
    meal.category=Category.objects.get(name=Inputs['category'])
    meal.save()
    return meal
    