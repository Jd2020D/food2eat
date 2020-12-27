from django.shortcuts import render,redirect
from django.http import JsonResponse

from . import models
from apps.restaurants_app.models import Meal
from django.contrib import messages


def mealsPage(request):  
    if 'id' not in request.session:
            return redirect('/')      
    if 'partner_id' in request.session:
        return redirect('/partner')
    if 'values' in request.session:
        del request.session['values']
    context={
        'meals':Meal.objects.all(),
        'orderedMealsIds':models.getOrderedMealsIds(request.session['id']),
        'quantities':models.getOrderedItemsQuantities(request.session['id'])
    }
    models.getOrdersHistory(request.session['id'])
    return render(request,'meals.html',context)

def cartPage(request):
    print(request.session['id'])
    if 'id' not in request.session or 'partner_id' in request.session :
                return redirect('/')
    if 'values' in request.session:
        del request.session['values']
    context={
        'items':models.getUserOrderedItems(request.session['id']),
        'total':models.getTotalCost(request.session['id'])
        
    }
    return render(request,'cart.html',context)

def addMealToCart(request):
    if not models.isMealOrdered(request.POST['meal_id'],request.session['id']):
        models.createItem(request.POST,request.session['id'])
    return JsonResponse({'id':int(request.POST['meal_id']),'action':'/meals/remove_from_cart','color':'red','value':'Remove'})

def removeMealFromCart(request):
    print(request.POST)
    if models.isMealOrdered(request.POST['meal_id'],request.session['id']):
        models.removeItem(request.POST,request.session['id'])
    return JsonResponse({'id':int(request.POST['meal_id']),'action':'/meals/add_to_cart','color':'#aad400','value':'Add','total_cost':models.getTotalCost(request.session['id'])})

def changeOrderQuantity(request,meal_id):
    if request.method=='POST':
        if models.isMealOrdered(meal_id,request.session['id']):
            item=models.changeOrderedItemQuantity(meal_id,request.session['id'],request.POST['quantity'])
            return JsonResponse({'id':item['id'],'item_cost':item['item_cost'],'total_cost':item['total_cost']})
        return JsonResponse({})       

def checkOut(request):
    if request.method=='POST':
        if 'id' in request.session and 'partner_id' not in request.session:
            if len(models.getUserOrderedItems(request.session['id'])):
                models.CreateNewOrder(request.session['id'])
            else:
                return JsonResponse({'error':'cart is empty!'})
            return redirect('/meals/cart')
    return redirect('/')

def viewHistory(request):
    if 'id' in request.session and 'partner_id' not in request.session:
        context={
                'orders':models.getAllOrders(request.session['id']),
                'history':models.getOrdersHistory(request.session['id']),
                'now_order':models.getOrderId(request.session['id'])
            }
        return render(request,'history.html',context)
    return redirect('/')