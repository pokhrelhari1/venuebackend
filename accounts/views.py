from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserFrom
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def registerPage(request):
    if request.method == "POST":
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            print(form.cleaned_data.get('first_name'))
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.contact = form.cleaned_data.get('contact')
            user.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password)
            # login(request, user)                                               # for logging in user after creating account
            context={'form':form}
            return redirect('login')

    else:
        form = CreateUserFrom()
    return render(request,'accounts/register.html', {'form': form})

        # if request.method =="POST":
        #     form= CreateUserFrom(request.POST)
        #     if form.is_valid():
        #         form.save()
        #         user = form.cleaned_data.get('username')
        #         messages.success(request,"Account was created for" + user) #flash message after creating the account successfully
                
        #         return redirect('login')

        # context={'form':form}
        # return render(request,'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method =="POST":
            username= request.POST.get('username')
            password= request.POST.get('password')

            user = authenticate(request, username= username, password= password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else: 
                messages.info(request,'Username or Password is incorrect')
                
        context={}
        return render(request,'accounts/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login') 
def index(request):
    return render(request,'accounts/index.html')

@login_required(login_url = 'login') 
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url = 'login') 
def customer(request):
    return render(request,'accounts/customer.html')
