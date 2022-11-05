from http.client import HTTPResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import todoForm, CreateUserForm
from .models import todo, User
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages 

#User=get_user_model()

# Create your views here

#login Page
def loginPage(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        #authenticate is used to verify a set of credentials-> it returns a User object if the credentials are valid
        user = authenticate(request, email=email, password=password)

        if user is not None:
            #login takes an HttpRequest object and a User object
            #we use backend so that when in future the same user logs in it fetchs the details
            login(request, user,backend=None)
            return redirect('add/')
        else:
            messages.info(request, 'Email Or password is incorrect')
    context={}
    return render(request, 'tasks/index.html', context)

#logout the user
def logoutUser(request):
    logout(request)
    return redirect('/')

#register Page
def registerPage(request): 
    form = CreateUserForm()
    if request.method == 'POST':
        print(request.POST)
        form= CreateUserForm(request.POST)
        print(form.is_valid())
        print(form)
        if form.is_valid():
            print("OP")
            form.save()
            user = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for '+ user)
            return redirect('add/')
    context={'form':form}
    return render(request, 'tasks/register.html', context)

#this function is used to save and show the tasks
def add(request):
    if request.method == 'POST':
        fm1=todoForm(request.POST, request.FILES)
        #method 1 to save the data(to save all the data)
        print('checkkk')
        if fm1.is_valid():
            print("validdd!!")
            fm1.save()
            #return redirect('/')

        #method 2 to save the data
        # if fm1.is_valid():
        #     name=fm1.cleaned_data['task']
        #     des=fm1.cleaned_data['description']
        #     tt=fm1.cleaned_data['time']
            # image=fm1.cleaned_data['quote']
            #date=fm1.cleaned_data['day']
            # newData = todo(task=name, description=des, time=tt )
            # newData.save()
            #fm1=todoForm() #it is used to clean the data and again prepare the form for new inputs
    else:
        fm1=todoForm()
    values=todo.objects.all()
    #print(dir(values[0].quote))
    return render(request,'tasks/add&show.html',{'form':fm1,'values':values})

#function to update the info
def update(request, id):
    #info=todo.objects.all()
    # info=todo.objects.filter(pk=id)
    #print("hiiii")
    # print(type(info))
    info=todo.objects.filter(pk=id).first()
    #form=todoForm(instance=info)
    if request.method=='POST':
        info=todo.objects.get(pk=id)
        form=todoForm(request.POST, instance=info)
        print(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('add/')
    #else:
    return render(request,'tasks/update.html',{'info':info})

#function to delete the task
def delete(request,pk):
    info=todo.objects.get(id=pk)
    if request.method=='POST':
        info.delete()
        return redirect('add/')
    context={
        'item':info
    }
    return render(request,'tasks/delete.html',context)