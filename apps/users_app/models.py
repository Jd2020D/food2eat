from django.db import models
import bcrypt
class UserRoll(models.Model):
    customer=models.BooleanField(default=True)
    partner=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
def intialize_rolls():
    rolls={}
    if len(UserRoll.objects.all())==0:
        rolls['customer_roll']=UserRoll.objects.create(customer=True,partner=False)
        rolls['partner_roll']=UserRoll.objects.create(customer=False,partner=True)
    else:
        rolls['customer_roll']=UserRoll.objects.get(customer=True)
        rolls['partner_roll']=UserRoll.objects.get(partner=True)
    return rolls
rolls=intialize_rolls()
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
    user.orders.all().delete()
    user.UserRoll=rolls['partner_roll']
    user.save()

    
def isPartner(id):
    user=User.objects.get(id=id)
    return user.userRoll.partner

def addUser(Inputs,asPartner=False):
    password = Inputs['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user_roll=rolls['customer_roll']
    if asPartner:
        user_roll=rolls['partner_roll']
    user=User.objects.create(userRoll=user_roll,first_name=Inputs['first_name'],last_name=Inputs['last_name'],user_name=Inputs['user_name'],phone_number=Inputs['phone_number'],address=Inputs['address'],email=Inputs['email'],password=pw_hash,birthDay=Inputs['birthDay'])
    if not asPartner:
        apps.orders_app.models.Order.objects.create(user=user)
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
    restaurant=apps.restaurants_app.models.Restaurant.objects.create(name=name,address=address,phoneNumber=phoneNumber,user=user)
    return restaurant.id

def checkPass(password,id):
    try:
        user=User.objects.get(id=id)
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return True
    except:
        pass
    return False

