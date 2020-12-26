from django.shortcuts import render,redirect
from django.http import JsonResponse

from . import models
from apps.restaurants_app.models import Meal
from django.contrib import messages


def mealsPage(request):
    if 'id' not in request.session or 'partner_id' in request.session :
                return redirect('/')
    if 'values' in request.session:
        del request.session['values']
    context={
        'meals':Meal.objects.all(),
        'orderedMealsIds':models.getOrderedMealsIds(request.session['id']),
        'quantities':models.getOrderedItemsQuantities(request.session['id'])
    }
    return render(request,'meals.html',context)

def cartPage(request):
    if 'id' not in request.session or 'partner_id' in request.session :
                return redirect('/')
    if 'values' in request.session:
        del request.session['values']
    total=0
    for total_price in [(item.meal.price*item.quantity) for item in models.getUserOrderedItems(request.session['id']) ]:
        total+=total_price
    context={
        'items':models.getUserOrderedItems(request.session['id']),
        'total':total
        
    }
    return render(request,'cart.html',context)

def addMealToCart(request):
    if not models.isMealOrdered(request.POST['meal_id'],request.session['id']):
        models.createItem(request.POST,request.session['id'])
    return JsonResponse({'id':int(request.POST['meal_id']),'action':'/meals/remove_from_cart','color':'red','value':'Remove'})

def removeMealFromCart(request):
    if models.isMealOrdered(request.POST['meal_id'],request.session['id']):
        print(models.removeItem(request.POST,request.session['id']))
    else:
        print('bow')
    return JsonResponse({'id':int(request.POST['meal_id']),'action':'/meals/add_to_cart','color':'#aad400','value':'Add'})

def changeOrderQuantity(request,meal_id):
    if request.method=='POST':
        item=models.changeOrderedItemQuantity(meal_id,request.session['id'],request.POST['quantity'])
    return JsonResponse({'id':item['id'],'total_price':item['total_price']})
        # models.changeOrderQuantity(meal_id,request.session['id'],request.)