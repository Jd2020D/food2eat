from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
import re
import datetime
import time


def register_valditor(Inputs):
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
    if models.getIdByEmail(Inputs['email']):
        errors['email_repeation']='There is an account with this email'
    if Inputs['password']!=Inputs['password_confirm']:
            errors['password_confirm']='password dosent match'
    if len(Inputs['password'])<8:
            errors['password']='password should be more than 8 characters'
    if len(Inputs['birthDay']) :
        secOfYear=31536000
        sec=time.time()-time.mktime(datetime.datetime.strptime(Inputs['birthDay'], "%Y-%m-%d").timetuple())
        if  sec <0:
            errors['birthDay']='Date should be in the past!'
        if sec/secOfYear <13:
            errors['age']='You are less than 13'
    else:
        errors['date']='Birthday date is required!'
    return errors

def login_valditor(Inputs,id):
    errors={}
    if not id:
        errors['email']='email is not found'
    elif not models.checkPass(Inputs['password'],id):
        errors['password']='password is not correct'
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
    return redirect ('/')
def viewAboutUs(request):
        return render(request, "aboutus.html")

def register(request):
    if request.method=='POST':
        print('signnnnnnnn')
        errors=register_valditor(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            request.session['action']='register'
            request.session['values']=request.POST
            print('errrrrrrrr')
        else:
            id=models.addUser(request.POST)
            request.session['id']=id
            request.session['name']=models.getNameById(id)
            messages.success(request, "successfully registerd")
            print('wow') 
            return redirect('/')       
    return redirect('/signup')

def login(request):
    if request.method=='POST':
        id=models.getIdByEmail(request.POST['email'])
        errors=login_valditor(request.POST,id)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            request.session['action']='logIn'
            request.session['values']=request.POST
        else:
            request.session['id']=id
            name=models.getNameById(id)
            request.session['name']=name
            messages.success(request, "successfully logged in")
            return redirect('/quotes')
    return redirect('/')


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
