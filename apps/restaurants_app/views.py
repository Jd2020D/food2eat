from django.contrib.messages.api import error
from django.shortcuts import render,redirect
from . import models
from django.contrib import messages

def clearTempSessions(request):
    if 'action' in request.session:
            del request.session['action']
    if 'values' in request.session:
        del request.session['values']

def partnerPage(request):
    # if 'id' not in request.session:
    #             return redirect('/signin')
    # if 'partner_id' not in request.session:
    #             return redirect('/signup/partner')
    clearTempSessions(request)
    return render(request,'dashboard.html')
    #pass
def addMeal_valditor(data):
    errors={}
    try:
        if len(data['title'])<2:
            errors['title_length'] ='title less than 2'
        if not (data['imgLink'].endswith('jpg') or data['imgLink'].endswith('png')):
            errors['imgLink'] ='please upload valid extintion'
    except:
        errors['invalid input']='dont change inputs'
    return errors
def addMeal(request):
    # if 'id' not in request.session:
    #             return redirect('/signin')
    # if 'partner_id' not in request.session:
    #             return redirect('/signup/partner')

    if request.method=='POST':
        errors=addMeal_valditor(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            request.session['values']=request.POST
        else:
            id=models.createMeal(request.POST,request.session.partner_id)
            return redirect('/partner')       
    return redirect('/')

