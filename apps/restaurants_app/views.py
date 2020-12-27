from django.contrib.messages.api import error
from django.shortcuts import render,redirect
from django.http import JsonResponse
from . import models
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def partnerPage(request):
    if 'id' not in request.session:
                return redirect('/signin')
    if 'partner_id' not in request.session:
                return redirect('/signup/partner')
    if 'values' in request.session:
            del request.session['values']
    context={
        'meals':models.getRestaurantMealsById(request.session['partner_id']),
        'categories':models.getCategories()
    }
    return render(request,'dashboard.html',context)
    #pass

def addMeal_valditor(data):
    errors={}
    try:
        if len(data['title'])<2:
            errors['title_length'] ='title less than 2'
        if len(data['description'])<8:
                errors['desc'] ='description less than 8'
        if len(data['description'])>96:
            errors['desc'] ='description more than 96'
        try:
            float(data['price'])
            if len(data['price'])<1:
                errors['price'] ='you cant buy something for free!'
        except:
            errors['price'] = 'Invalid entered price'            
         
        if not (data['imgLink'].endswith('jpg') or data['imgLink'].endswith('png')):
            errors['imgLink'] ='please put valid link extintion ends with png or jpg'
    except:
        errors['invalid input']='dont change inputs'
    return errors

def addMeal(request):
    if 'id' not in request.session:
                return redirect('/signin')
    if 'partner_id' not in request.session:
                return redirect('/signup/partner')
    if request.method=='POST':
        errors=addMeal_valditor(request.POST)
        if len(errors) > 0:
            request.session['values']=request.POST
            return JsonResponse({'errors':errors})
        else:
            meal=models.createMeal(request.POST,request.session['partner_id'])
            imgLink=meal.imgLink
            iconLink=meal.category.iconLink
            if not imgLink.startswith('http'):
                imgLink='/static/img/'+imgLink
            if not iconLink.startswith('http'):
                iconLink='/static/img/'+iconLink

            html=f"""
            <section  id='view_{meal.id}'>
      <form action='/partner/editMeal' method='post' class='mealViewer mealView'>
        <h3>{meal.title}<img src='{imgLink}' alt='meal image'></h3>
        <aside>
          <img src="{iconLink}" alt='icon'>
          <p>{meal.description}</p>
            <nav>
              <p>{meal.price} NIS</p>
              <input type=hidden name='meal_id' value='{meal.id}'>
              <input type='submit' value='Edit'>
              <button class='delete_from_re' id='delete_{meal.id}' >Delete</button>
                <p>{meal.category.name}</p>
            </nav>  
        </aside>
      </form>  
    </section>

        """
            return JsonResponse({'id':meal.id,'html':html})
    return redirect('/')

def removeMealFromPartner(request):
    if models.getMealById(request.POST['meal_id'],request.session['partner_id']):
        models.removeMealFromPartner(request.POST['meal_id'],request.session['partner_id'])
    return JsonResponse({'id':request.POST['meal_id']})

@csrf_exempt
def editMeal(request):
    if 'id' not in request.session:
            return redirect('/signin')
    if 'partner_id' not in request.session:
                return redirect('/signup/partner')
    if request.method=='POST':
        errors={}
        if not models.getMealById(request.POST['meal_id'],request.session['partner_id']):
            errors={'change in inputs':'dont change hidden inputs!!!'}
        if len(errors) > 0:
            request.session['values']=request.POST
            return JsonResponse({'id':request.POST['meal_id'],'errors':errors})
        else:
            meal=models.getMealById(request.POST['meal_id'],request.session['partner_id'])
            iconLink=meal.category.iconLink
            if not iconLink.startswith('http'):
                    iconLink='/static/img/'+iconLink
            html=f"""    
                    <section>
                        <form action='/partner/updateMeal' method='post' id='mealEdit_{meal.id}' class='mealEdit mealViewer'>
                            <h3>
                            <input type=text name='title' value="{meal.title}">
                            <label>Image Link</label>
                            <input type='text' name='imgLink' value="{meal.imgLink}">
                            </h3>
                            <aside>
                            <img src='{iconLink}' alt='#'>
                            <p><textarea name='description' >{meal.description}</textarea></p>
                                <nav>
                                <p>Price: </p>
                                <p><input type='text' name='price'  value="{meal.price}"> NIS</p>
                                <select name='category' >
                """
            b=''
            for category in models.getCategories():
                b+='<option>'+category.name+'</option>'
            b+=f"""
                </select>
                    <input type=hidden name='meal_id' value='{meal.id}'>
                <input type='submit' value='Update'>
                </nav>  
                    </aside>
                </form>  
            </section>
            """
            html+=b
            return JsonResponse({'id':request.POST['meal_id'],'html':html})

def updateMeal_valditor(Inputs,partner_id):
    errors=addMeal_valditor(Inputs)
    if not models.getMealById(Inputs['meal_id'],partner_id):
        errors['you are not owner']='cant edit others meals!!'
    return errors
@csrf_exempt
def updateMeal(request):
    if 'id' not in request.session:
                return redirect('/signin')
    if 'partner_id' not in request.session:
                return redirect('/signup/partner')
    if request.method=='POST':
        errors=updateMeal_valditor(request.POST,request.session['partner_id'])
        if len(errors) > 0:
            request.session['values']=request.POST
            return JsonResponse({'errors':errors})
        else:
            meal=models.updateMeal(request.POST)
            imgLink=meal.imgLink
            iconLink=meal.category.iconLink
            if not imgLink.startswith('http'):
                imgLink='/static/img/'+imgLink
            if not iconLink.startswith('http'):
                iconLink='/static/img/'+iconLink

            html=f"""
                <section  id='view_{meal.id}'>
        <form action='/partner/editMeal' method='post' class='mealViewer mealView'>
            <h3>{meal.title}<img src='{imgLink}' alt='meal image'></h3>
            <aside>
            <img src="{iconLink}" alt='icon'>
            <p class='mealDesc'>{meal.description}</p>
                <nav>
                <p>{meal.price} NIS</p>
                <input type=hidden name='meal_id' value='{meal.id}'>
                <input type='submit' value='Edit'>
                <button class='delete_from_re' id='delete_{meal.id}' >Delete</button>
                    <p>{meal.category.name}</p>
                </nav>  
            </aside>
        </form>  
        </section>

            """
            return JsonResponse({'id':request.POST['meal_id'],'html':html})
    return JsonResponse({})