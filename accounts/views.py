from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserFrom, CustomerForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import unauthenticated_user,allowed_users,admin_only
from .filters import locationFilter

from rest_framework import viewsets
from .serializer import VenueSerializer, CateringSerializer, PaymentSerializer, FeedbackSerializer, extraServiceSerializer, BookingSerializer, UserSerializer


@unauthenticated_user
def registerPage(request):
    if request.method == "POST":
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.username= form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            user.profile.first_name = form.cleaned_data.get('first_name')
            print(form.cleaned_data.get('first_name'))
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.contact = form.cleaned_data.get('contact')
            user.profile.profile_picture = form.cleaned_data.get('profile_picture')
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


# class userEditForm(generic.CreateView):
#     form= userEditForm(request.POST)
#     template_name= 'accounts/updateProfile'
#     success_url = reverse_lazy('')

@unauthenticated_user
def loginPage(request):
    if request.method =="POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        print(username)
        print(password)

        user = authenticate(request, username= username, password= password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:   
            messages.info(request,'Username or Password is incorrect')      
    return render(request,'accounts/login.html')


def logoutUser(request):
    logout(request) 
    return redirect('login')


def index(request):
    venue = Venue.objects.all()
    myFilter= locationFilter( request.GET, queryset= venue)
    venue = myFilter.queryset
    return render(request,'accounts/index.html', {'venue': venue ,'myFilter':myFilter})

@login_required(login_url = 'login')
@admin_only #calling the decoratior  for page permission
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


#function for user profile
@login_required(login_url='login')
def userProfile(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    form = CustomerForm(instance= profile)
    context= {'form':form}
    return render(request,'accounts/userProfile.html',context)

#fuction to update user profile
@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    profile = get_object_or_404(Profile, user = user)
    form = CustomerForm(instance = profile)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.email = form.cleaned_data.get('email')
            profile.contact = form.cleaned_data.get('contact')
            profile.profile_picture = request.FILES['profile_picture']
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            profile.save()
            user.save()
            return redirect('userProfile')
    context = {'form':form}
    return render(request,'accounts/updateProfile.html', context)
   
#function to render venue details.
@login_required(login_url='login')
def viewDetail(request, id):
    venue= Venue.objects.get(pk=id)
    photos = venueImage.objects.filter(venue= venue)
    context={
        'venue':venue,
        'photos':photos 
        }
    return render(request,'accounts/viewDetail.html',context)
    
def bookingForm(request):
    return render(request, 'accounts/bookingForm.html')


#viewset for api
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

class VenueView(viewsets.ModelViewSet):
    queryset= Venue.objects.all()
    serializer_class = VenueSerializer

class PaymentView(viewsets.ModelViewSet):
    queryset= Payment.objects.all()
    serializer_class= PaymentSerializer

class FeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class CateringView(viewsets.ModelViewSet):
    queryset = Catering.objects.all()
    serializer_class = CateringSerializer

class BookingView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class extraServiceView(viewsets.ModelViewSet):
    queryset = extraService.objects.all()
    serializer_class = extraServiceSerializer