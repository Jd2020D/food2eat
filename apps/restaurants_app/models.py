from django.db import models
from apps.users_app.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    user=models.ForeignKey(User, on_delete = models.CASCADE)
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
#as