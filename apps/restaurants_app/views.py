from django.shortcuts import render,redirect
from . import models
from django.contrib import messages


def partnerPage(request):
    if 'id' not in request.session:
                return redirect('/')
    if 'action' in request.session:
            del request.session['action']
    if 'values' in request.session:
        del request.session['values']
    # return render(request,'quotes_page.html',context)
    #pass
