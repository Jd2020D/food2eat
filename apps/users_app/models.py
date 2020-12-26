from django.db import models
import apps.orders_app.models as orders_models
import apps.restaurants_app.models as restu_models

import bcrypt
class UserRoll(models.Model):
    customer=models.BooleanField(default=True)
    partner=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    userRoll=models.ForeignKey(UserRoll,related_name="users", on_delete = models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    phone_number=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    birthDay=   models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def TransferCustomerToPartner(id):
    user=User.objects.get(id=id)
    user.UserRoll.customer=False
    user.orders.all().delete()
    user.UserRoll.partner=True
    
def isPartner(id):
    user=User.objects.get(id=id)
    return user.userRoll.partner#wwwwwwwwww

def addUser(Inputs,asPartner=False):
    password = Inputs['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user_roll=UserRoll(customer=True,partner=False)
    if asPartner:
        user_roll.customer=False
        user_roll.partner=True
    user=User.objects.create(userRoll=user_roll,first_name=Inputs['first_name'],last_name=Inputs['last_name'],user_name=Inputs['user_name'],phone_number=Inputs['phone_number'],address=Inputs['address'],email=Inputs['email'],password=pw_hash,birthDay=Inputs['birthDay'])
    if not asPartner:
        orders_models.Order.objects.create(user=user)
    return user.id

def getNameById(id):
    user=User.objects.get(id=id)
    return user.first_name+" "+user.last_name

def getEmailAndName(id):
    user=User.objects.get(id=id)
    return {
        'first_name':user.first_name,
        'last_name':user.last_name,
        'email':user.email
    }
def updateAccount(Inputs,id):
    user=User.objects.get(id=id)
    user.first_name=Inputs['first_name']
    user.last_name=Inputs['last_name']
    user.email=Inputs['email']
    user.save()
    return user.first_name+" "+user.last_name
def getIdByEmail(email):
    try:
        user=User.objects.get(email=email)
        return user.id
    except:
        return False

def getEmailById(id):
    return User.objects.get(id=id).email
def isEmailDuplicate(email):
    try:
        User.objects.get(email=email)
        return True
    except:
        return False

def createRestaurant(name,address,phoneNumber,user_id):
    user=User.objects.get(id=user_id)
    restaurant=restu_models.Restaurant.objects.create(name=name,address=address,phoneNumber=phoneNumber,user=user)
    return restaurant.id

def checkPass(password,id):
    try:
        user=User.objects.get(id=id)
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return True
    except:
        pass
    return False

