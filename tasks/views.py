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
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username Or password is incorrect')
    context={}
    return render(request, 'tasks/index.html', context)

#logout the user
def logoutUser(request):
    logout(request)
    return redirect('login')

#register Page
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+ user)

            return redirect('login')
    context={'form':form}
    return render(request, 'tasks/register.html', context)

#this function is used to save and show the tasks
def add(request):
    if request.method == 'POST':
        fm1=todoForm(request.POST, request.FILES)
        #method 1 to save the data(to save all the data)
        if fm1.is_valid():
            fm1.save()
            return redirect('/')

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
    print(dir(values[0].quote))
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
            return redirect('/')
    #else:
    return render(request,'tasks/update.html',{'info':info})

#function to delete the task
def delete(request,pk):
    info=todo.objects.get(id=pk)
    if request.method=='POST':
        info.delete()
        return redirect('/')
    context={
        'item':info
    }
    return render(request,'tasks/delete.html',context)