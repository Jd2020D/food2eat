from django.shortcuts import render,redirect
from django.http import JsonResponse

from . import models
from django.contrib import messages


def mealsPage(request):
    # if 'id' not in request.session or 'partner_id' in request.session :
    #             return redirect('/')
    if 'values' in request.session:
        del request.session['values']
    return render(request,'meals.html')
    #pass
def addMealToCart(request):
    return JsonResponse({'add':1})