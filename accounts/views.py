from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserFrom, CustomerForm, bookingForm,cateringForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import unauthenticated_user,allowed_users,admin_only
from .filters import locationFilter
from django.views import View
from django.db import models

from rest_framework import viewsets
from .serializer import VenueSerializer, CateringSerializer, PaymentSerializer, FeedbackSerializer, extraServiceSerializer, BookingSerializer, UserSerializer, food_PackageSerializer, Menu_ItemsSerializer, CatogerySerializer, venueImageSerializer, VendorRequestSerializer

import requests
import json

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
        # print(username)
        # print(password)

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
    venue= myFilter.qs
    venue = myFilter.queryset
    return render(request,'accounts/index.html', {'venue': venue ,'myFilter':myFilter})


#search bar functions
# def searchbar(request):
  
#     return render(request, 'accounts/searchBAR.html')


    # if request.method== 'GET':
    #     search = request.GET.get('search')
    #     venue = Venue.objects.all().filter(address=search)
    #     return render(request,'searchbar.html', { 'venue':venue})


# def index(request):
#     catering = Catering.objects.all()
#     myFilter= locationFilter( request.GET, queryset= cateirng)
#     catering = myFilter.queryset
#     return render(request,'accounts/index.html', {'catering': catering ,'myFilter':myFilter})


@login_required(login_url = 'login')
@admin_only #calling the decoratior  for page permission
def adminDashboard(request):
    
    vendor_request_data = requests.get("http://127.0.0.1:8000/vendor-request/").content
    vendor_request_data = json.loads(vendor_request_data)
    if request.method == 'GET':
        print("vendor requests", type(vendor_request_data), vendor_request_data)
        return render(request, 'accounts/adminDashboard.html', context = {'vendor_request': vendor_request_data})
    if request.method == 'POST':
        
        # send email to user that your request has been accepted
        print("request approved", request.POST.get('hidden-id'))
        request_id = request.POST.get('hidden-id')
        vend_req = VendorRequest.objects.get(id = request_id)
        vend_req.is_accepted = True
        vend_req.save()
        vendor_request_data = requests.get("http://127.0.0.1:8000/vendor-request/").content
        vendor_request_data = json.loads(vendor_request_data)
        print("vendor req data", vendor_request_data)
        return render(request, 'accounts/adminDashboard.html', context = {'vendor_request': vendor_request_data})


#function for user profile
@login_required(login_url='login')
def userProfile(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    form = CustomerForm(instance= profile)
    # booking = user.book_set.all()
    booking_done = Booking.objects.filter(customer= request.user.profile)
    context= {'form':form, 'booking_done': booking_done}
    return render(request,'accounts/userProfile.html',context)


@login_required(login_url='login')
def userDashboard(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    form = CustomerForm(instance= profile)
    # booking = user.book_set.all()
    booking_done = Booking.objects.filter(customer= request.user.profile)
    context= {'form':form, 'booking_done': booking_done}
    return render(request,'accounts/userDashboard.html',context)

@login_required(login_url='login')
def viewBookingDetails(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    form = CustomerForm(instance= profile)
    # booking = user.book_set.all()
    booking_done = Booking.objects.filter(customer= request.user.profile)
    context= {'form':form, 'booking_done': booking_done}
    return render(request,'accounts/viewBookingDetails.html',context)

    
#function to delete booking history for user
def deleteBooking(request, id):
    booking = Booking.objects.get(pk=id)
    if request.method == "POST":
        booking.delete()
        return redirect('userProfile')
    return render(request, 'accounts/deleteBooking.html')

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

# def searchbar(request):
#     venue_list= Venue.objects.all()
#     locationFilter = location_filter(request.GET, queryset= venue_list) 
#     return render(request,'accounts/searchbar.html')

def searchbar(request):
    return render(request,'accounts/searchbar.html')
    

#use dropdown for district and filter the place with autocomplete
def searchLocation(request):
    if request.method == 'POST':
        input_data = request.POST
        print("Input data", input_data)
        input_address = input_data['search-address']
        input_district = input_data['search-district']
        print("input", input_address, input_district)

        data = Venue.objects.filter(address = input_address).filter(district = input_district)
        if Venue.objects.filter(address = input_address).filter(district = input_district).exists():
            print("location filter", input_data)

    return render(request, 'accounts/searchbar.html', context = {'data': data})


def filter_venue(request):
    price= request.GET.getlist('price')
    max_guestCapacity= request.GET.getlist('max_guestCapacity')
    filterVenue = Venue.objects.filter(
        # price__id__in= price,
        # max_guestCapacity__id__in= max_guestCapacity,
        price = price,
        max_guestCapacity= max_guestCapacity,
    )
    # return HttpResponse(filterVenue.query)
    return render(request,'accounts/filter_venue.html', context= {'filterVenue':filterVenue})



def add_venue(request):
    return render(request, 'accounts/add_venue.html')
   
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


def tables(request):
    return render(request,'accounts/tables.html')

def vendorRequest(request):
    return render(request,'accounts/vendorRequest.html')

    
def booking(request, id):

    # caterings = Catering.objects.all()
    # food_packages = food_Package.objects.all()
    categories = Category.objects.all()

    if request.method== 'POST':
        form  =  bookingForm(request.POST)
        print(form.errors)
        if form.is_valid():
            book = form.save(commit=False)
            book.customer = request.user.profile
            book.venue = Venue.objects.get(id=id)
            book.foodpackage = OrderedFoodPackage.objects.get(packageName=str(request.user.id))


            # package = request.POST.getlist('package')    
         
            # host = request.POST.getlist('host')
            # music = request.POST.getlist('music')
            # if response.POST.get('submit'):
            #     for item in item_set.all():
            #         if response.POST.get("package1" + str(item.id))=="clicked":
            #             item.complete = True
            #         else: 
            #             item.complete = False
            #         item.save()
            # book.catering = Catering.objects.get(id=id)
            book.save()
           
            redirect('/bookingForm/')
            
         

           
    else:
        
        form = bookingForm()
    return render(request, 'accounts/bookingForm.html', {'form':form,'categories':categories})


# def cateirng(request):
#     if request.method =='POST':
#         form= cateringForm(request.POST)
#         if form.is_valid():
#             catering = form.cleaned_data.get('catering')
#     else:
#         form = cateirng
#     return render('accounts/bookingForm.html', {'form': form})     #render_to_response le k garxa?s

# use model panel for food selection
def food_package_menu(request, id):
    all_items = Menu_Items.objects.filter(category__id=id)

    if request.method == "POST":
        selected_items = request.POST.getlist('items')
        orderedpackage = OrderedFoodPackage()
        orderedpackage.packageName=str(request.user.id)
        orderedpackage.price=100          #adding price to menu_list table 
        orderedpackage.save()
        # for item in selected_items:
        #     menu_item = Menu_Items.objects.filter(id=item)
        orderedpackage.Menu_Items.set(selected_items)
        
        return render(request,'accounts/bookingForm.html')


    return render(request,'accounts/foodordermenu.html',{'items':all_items})


# def filter_data(request):
#     all_data = data.objects.filter(price=id)
#     price1= request.GET.getlist('price1')
#     price2= request.GET.getlist('price2')
#     price3= request.GET.getlist('price3')



class catering(View):
    def get(self,request, *args, **kwargs):
        appetizers = Menu_Items.objects.filter(category__name__contains='Appetizers')
        print(appetizers)
        mainCourse = Menu_Items.objects.filter(category__name__contains='MainCourse')
        dessert = Menu_Items.objects.filter(category__name__contains='Dessert')
        drink = Menu_Items.objects.filter(category__name__contains='Drink')

        #pass into context

        context ={
            'appetizers': appetizers,
            'mainCourse':mainCourse,
            'dessert': dessert,
            'drink': drink,

        }

        return render(request,'accounts/catering.html', context)

    def post(self, request, *args, **kwargs):
        catering_items={
            'items': []
        }
        
        items = request.POST.getlist('items')

        for item in items:
            print("Im a item")
            menu_item = Menu_Items.objects.get(id= int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
               

            }
            catering_items['items'].append(item_data)

        # price = 0
        # item_ids =[]

        # for item in catering_items['items']:
        #     price += item['price']
        #     item_ids.append(item['id'])

        # catering = Catering.objects.create(price= price)
        # catering.items.add(*item_ids)
        # catering.save()

        # context ={
        #     'items': catering_items['items'],
        #     'price': price

        # }

        return render(request,'accounts/bookingForm.html')





#viewset for api
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

class VenueView(viewsets.ModelViewSet):
    queryset= Venue.objects.all()
    serializer_class = VenueSerializer

class venueImageView(viewsets.ModelViewSet):
    queryset= venueImage.objects.all()
    serializer_class = venueImageSerializer

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

class food_PackageView(viewsets.ModelViewSet):
    queryset = food_Package.objects.all()
    serializer_class = food_PackageSerializer



class Menu_ItemsView(viewsets.ModelViewSet):
    queryset = Menu_Items.objects.all()
    serializer_class = Menu_ItemsSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CatogerySerializer


class VendorRequestViewset(viewsets.ModelViewSet):
    queryset = VendorRequest.objects.all()
    serializer_class = VendorRequestSerializer



