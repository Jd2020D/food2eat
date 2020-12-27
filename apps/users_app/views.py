from django.shortcuts import render,redirect
from django.http import JsonResponse

from . import models
from django.contrib import messages
import re
import datetime
import time
import apps.restaurants_app.models

# def checkFirstname(request):
#     print(request.POST)
#     errors={}
#     if len(request.POST['first_name']) <2:
#         errors['first_name_len']='First name should be more than 2 characters'
#     return JsonResponse({'errors':errors,'id':'first_name'})

def register_valditor(Inputs):
    errors={'first_name':[],
            'last_name':[],
            'user_name':[],
            'address':[],
            'phone_number':[],
            'email':[],
            'password':[],
            'birthDay':[],
            'password_confirm':[]
    }
    name_regex=re.compile("^[a-zA-Z]+$")
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(Inputs['first_name']) <2:
        errors['first_name'].append('First name should be more than 2 characters')
    if name_regex.match(Inputs['first_name']) is None:
        errors['first_name'].append('Invalid First Name')
    if len(Inputs['last_name']) <2:
        errors['last_name'].append('Last name should be more than 2 characters')
    if name_regex.match(Inputs['last_name']) is None:
        errors['last_name'].append('Invalid Last Name')
    if len(Inputs['user_name']) <2:
        errors['user_name'].append('user name should be more than 2 characters')
    if name_regex.match(Inputs['user_name']) is None:
        errors['user_name'].append('Invalid User Name')
    if models.getIdByUserName(Inputs['user_name']):
        errors['user_name'].append('There is an account with this user name')
    if len(Inputs['address']) <2:
        errors['address'].append('address should be more than 2 characters')
    if name_regex.match(Inputs['address']) is None:
        errors['address'].append('Invalid address')
    if len(Inputs['phone_number']) <9:
        errors['phone_number'].append('phone_number should be 10 numbers')
    if name_regex.match(Inputs['address']) is None:
        errors['address'].append('Invalid phone_number')
    if not EMAIL_REGEX.match(Inputs['email']):
        errors['email'].append('Invalid Format')
    if models.getIdByEmail(Inputs['email']):
        errors['email'].append('There is an account with this email')
    if Inputs['password']!=Inputs['password_confirm']:
            errors['password_confirm'].append('password dosent match')
    if len(Inputs['password'])<8:
            errors['password'].append('password should be more than 8 characters')
    if len(Inputs['birthDay']) :
        secOfYear=31536000
        sec=time.time()-time.mktime(datetime.datetime.strptime(Inputs['birthDay'], "%Y-%m-%d").timetuple())
        if  sec <0:
            errors['birthDay'].append('Date should be in the past!')
        if sec/secOfYear <13:
            errors['birthDay'].append('You are less than 13')
    else:
        errors['birthDay'].append('Birthday date is required!')
    return errors



def login_valditor(Inputs,id):
    errors={
        'email':[],
        'password':[],
    }
    if not id:
        errors['email'].append('email is not found')
    elif not models.checkPass(Inputs['password'],id):
        errors['password'].append('password is not correct')
    return errors

def root(request):
        return render(request, "main.html")

def viewSignInPage(request):
    if id in request.session:
        return redirect('/')
    if 'action' not in request.session:
                request.session['action']=''
    if 'values' not in request.session:
            request.session['values']={}
    context={
            'action':request.session['action'],
            'values':request.session['values']
        }
    del request.session['action']
    del request.session['values']
    return render(request, "signin.html",context)


def viewSignUpPage(request):
    if id in request.session:
        return redirect('/')
    if 'action' not in request.session:
                request.session['action']=''
    if 'values' not in request.session:
            request.session['values']={}
    context={
            'action':request.session['action'],
            'values':request.session['values']
        }
    del request.session['action']
    del request.session['values']
    return render(request, "register.html",context)

def viewSignUpPartnerPage(request):
    if id in request.session and models.isPartner(request.session[id]):
        return redirect('/')
    return render(request,'register_partner.html')
        
def contactResult(request):
    return render(request, "email_received.html")
    
def viewAboutUs(request):
        return render(request, "aboutus.html")

def register(request):
    if request.method=='POST':
        errors=register_valditor(request.POST)
        error_exist=False
        for error in errors:
            if len(error)>0:
                error_exist=True
        if error_exist:
            for value in errors.values():
                messages.error(request, value)
            request.session['values']=request.POST
            return JsonResponse(errors)
        else:
            id=models.addUser(request.POST)
            request.session['id']=id
            request.session['name']=models.getNameById(id)
            messages.success(request, "successfully registerd")
            return JsonResponse({"redirect_url":"/"})       
    return redirect('/signup')

def registerSubmit(request):
    if request.method=='POST':
        errors=register_valditor(request.POST)
        error_exist=False
        for error in errors:
            if len(errors[error])>0:
                print(len(error))
                error_exist=True
        if error_exist:
            for value in errors.values():
                print(value)
                messages.error(request, value)
            request.session['values']=request.POST
        else:
            id=models.addUser(request.POST)
            request.session['id']=id
            request.session['name']=models.getNameById(id)
            messages.success(request, "successfully registerd")
            return redirect("/")       
    return redirect('/signup')

def register_partner(request):
    if request.method=='POST':
        errors=register_valditor(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            request.session['values']=request.POST
        else:
            id=models.addUser(request.POST,asPartner=True)
            request.session['id']=id
            request.session['partner_id']=apps.restaurants_app.models.createRestaurant(name=request.POST['name'],address=request.POST['address'],phoneNumber=request.POST['phoneNumber'],user_id=id)
            #add the other attributes here
            request.session['name']=models.getNameById(id)
            messages.success(request, "successfully registerd")
            return redirect('/')       
    return redirect('/signup')

def login(request):
    if request.method=='POST':
        id=models.getIdByEmail(request.POST['email'])
        errors=login_valditor(request.POST,id)
        error_exist=False
        for error in errors:
            if len(errors) > 0:
                error_exist=True
        if error_exist:
            for value in errors.values():
                messages.error(request, value)
            request.session['values']=request.POST
            return JsonResponse(errors)
        else:
            request.session['id']=id
            name=models.getNameById(id)
            request.session['name']=name
            messages.success(request, "successfully logged in")
            return JsonResponse({"redirect_url":"/"})
    return redirect('/signin')

def loginSubmit(request):
    if request.method=='POST':
        id=models.getIdByEmail(request.POST['email'])
        errors=login_valditor(request.POST,id)
        error_exist=False
        for error in errors:
            if len(errors[error]) > 0:
                error_exist=True
        if error_exist:
            for value in errors.values():
                messages.error(request, value)
            request.session['values']=request.POST
        else:
            request.session['id']=id
            name=models.getNameById(id)
            request.session['name']=name
            messages.success(request, "successfully logged in")
            return redirect("/")
    return redirect('/signin')


def editAccountPage(request):
    data= models.getEmailAndName(request.session['id'])
    context={
        'first_name':data['first_name'],
        'last_name':data['last_name'],
        'email':data['email'],
    }

    return render(request,'updatePage.html',context)

def update_valditor(Inputs,id):
    errors={}
    name_regex=re.compile("^[a-zA-Z]+$")
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(Inputs['first_name']) <2:
        errors['first_name_len']='First name should be more than 2 characters'
    if name_regex.match(Inputs['first_name']) is None:
        errors['first_name']='Invalid First Name'
    if len(Inputs['last_name']) <2:
        errors['last_name_len']='Last name should be more than 2 characters'
    if name_regex.match(Inputs['last_name']) is None:
        errors['last_name']='Invalid Last Name'
    if not EMAIL_REGEX.match(Inputs['email']):
        errors['email']='Invalid Format'    
    if models.getIdByEmail(Inputs['email']) and Inputs['email']!=models.getEmailById(id) :
        errors['email_repeation']='There is an account with this email'
    return errors

def updateAccount(request):
    if request.method=='POST':
        errors=update_valditor(request.POST,request.session['id'])
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
        else:
            newName=models.updateAccount(request.POST,request.session['id'])
            request.session['name']=newName
            messages.success(request, "successfully updated")
    return redirect('/myaccount')
    

def logout(request):
    if 'id' in request.session :
        del request.session['id']
    if 'name' in request.session:
        del request.session['name']
    return redirect('/')

# Create your views here.
