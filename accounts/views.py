from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserFrom, CustomerForm, bookingForm,cateringForm, venueForm, venueImageForm, extraServiceForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import unauthenticated_user,allowed_users,admin_only
from .filters import locationFilter
from django.views import View
from django.db import models
from django.forms import ModelForm
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic.edit import UpdateView
from django.db import transaction



from django.http import QueryDict

from rest_framework import viewsets
from .serializer import InquirySerializer, VenueSerializer, CateringSerializer, PaymentSerializer, FeedbackSerializer, extraServiceSerializer, BookingSerializer, UserSerializer, food_PackageSerializer, Menu_ItemsSerializer, CatogerySerializer, venueImageSerializer, VendorRequestSerializer

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
def vendorRequest(request):
    if request.method=="POST":
        venue_name = request.POST.get('venue_name')
        request_description = request.POST.get('request_description')
        email = request.POST.get('email')
        req_from= request.POST.get('req_from')
        user_name = request.POST.get('user_name')
        data= data={'venue_name':venue_name, 'request_description': request_description, 'email': email, 'req_from':req_from, 'user_name': user_name}
        headers= {'Content-Type': 'application/json'}
        print("vendor request-------------", data)
        read= requests.post('http://127.0.0.1:8000/vendor-request/', json=data, headers=headers)
        return render(request, 'accounts/vendorRequest.html')
       
    else:
        return render(request,'accounts/vendorRequest.html')
        
  



@login_required(login_url = 'login')
@admin_only #calling the decoratior  for page permission
# def adminDashboard(request):
    
#     vendor_request_data = requests.get("http://127.0.0.1:8000/vendor-request/").content
#     vendor_request_data = json.loads(vendor_request_data)
#     if request.method == 'GET':
#         print("vendor requests", type(vendor_request_data), vendor_request_data)
#         return render(request, 'accounts/adminDashboard.html', context = {'inquiry': vendor_request_data})
#     if request.method == 'POST':
        
#         # send email to user that your request has been accepted
#         print("request approved", request.POST.get('hidden-id'))
#         request_id = request.POST.get('hidden-id')
#         vend_req = VendorRequest.objects.get(id = request_id)
#         vend_req.is_accepted = True
#         vend_req.save()
#         vendor_request_data = requests.get("http://127.0.0.1:8000/vendor-request/").content
#         vendor_request_data = json.loads(vendor_request_data)
#         print("vendor req data", vendor_request_data)
#         return render(request, 'accounts/adminDashboard.html', context = {'inquiry': vendor_request_data})

def adminDashboard(request):
    user_count= User.objects.all().count()
    venue_count= Venue.objects.all().count()
    vendorRequest_count= Inquiry.objects.all().count()
    booking_count= Booking.objects.all().count()
    inquiry = Inquiry.objects.all()
    return render(request,'accounts/adminDashboard.html', {'inquiry':inquiry,
         'user_count':user_count,
         'venue_count':venue_count,
         'vendorRequest_count':vendorRequest_count, 
         'booking_count':booking_count, } )

# def status(request):
#     user_count= User.objects.count()
#     venue_count= Venue.objects.count()
#     vendorRequest_count= VendorRequest.objects.count()
#     booking_count= Booking.objects.count()
    
#     return render(request,'accounts/adminDashboard.html',{
#          'user_count':user_count,
#          'venue_count':venue_count,
#          'vendorRequest_count':vendorRequest_count, 
#          'booking_count':booking_count, 
         
#      })

   
# finction for edit venue table

def editVenue(request,id):
    venue= Venue.objects.get(pk=id)
    form = venueForm(instance=venue)
    
    if request.method == "POST":
        # form = venueForm(request.POST, request.FILES)
        obj = get_object_or_404(Venue, id = id)
        form = venueForm(request.POST or None, instance = obj)
        # print(request.POST)
        # print("Inside post")
        print(form.errors)
        # print("error")
        if form.is_valid():
            print("Valid form")
            form.save()
            return redirect('venueTable')
    context={
        'venue':venue,
        'form':form,
        }
    return render(request,'accounts/editVenue.html',context)
    


# def updateVenue(request,id):

#     context ={}
#     obj = get_object_or_404(Venue, id = id)

#     form = venueForm(request.POST or None, instance = obj)

#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect("/"+id)
#     context["form"] = form
  
#     return render(request, "venueTable.html", context)




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
def viewBookingDetails(request, id):
    user = request.user
    profile = Profile.objects.get(user = user)
    form = CustomerForm(instance= profile)
    # booking = user.book_set.all()
    booking_done = Booking.objects.filter(customer= request.user.profile, id=id)
    context= {'form':form, 'booking_done': booking_done}
    return render(request,'accounts/viewBookingDetails.html',context)

    
#function to delete booking history for user
def deleteBooking(request, id):
    booking = Booking.objects.get(pk=id)
    if request.method == "POST":
        booking.delete()
        return redirect('userProfile')
    return render(request, 'accounts/deleteBooking.html')

#function to delete venue
def deleteVenue(request,id):
    venue = Venue.objects.get(pk=id)
    if request.method == "POST":
        venue.delete()
        return redirect('venueTable')
    return render(request, "accounts/deleteVenue.html")

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
    venue= Venue.objects.all()
    return render(request,'accounts/searchbar.html', {'venue':venue})
    

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

    return render(request, 'accounts/searchbar.html', context = {'data': data, 'venue':venue})


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

# def vendorRequest(request):
#     return render(request,'accounts/vendorRequest.html')

    
@transaction.atomic    
def booking(request, id):

    # caterings = Catering.objects.all()
    # food_packages = food_Package.objects.all()
    categories = Category.objects.all()
    all_items = Menu_Items.objects.all()

    if request.method== 'POST':
        form  =  bookingForm(request.POST)
        items = request.POST.getlist('item_checkbox')
        package = request.POST.getlist('package_checkbox')[0]
        if not items:
            items = Menu_Items.objects.filter(category__name=package)
        if form.is_valid():
            book = form.save(commit=False)
            book.customer = request.user.profile
            book.venue = Venue.objects.get(id=id)
            orderedpackage = OrderedFoodPackage()
            orderedpackage.packageName=package + "-" +str(request.user.profile)
            orderedpackage.price=100          #adding price to menu_list table 
            orderedpackage.save()
            orderedpackage.Menu_Items.set(items)
            book.foodpackage = orderedpackage
            book.save()
           
            return redirect('/payment/')
            # return HttpResponse("Success")
    else:
        
        form = bookingForm()
    context = {
        'form':form,
        'categories':categories,
        'all_items':all_items,
    }
    return render(request, 'accounts/bookingForm.html', context)

def inquiry(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        venue_name = request.POST.get('venue_name')
        request_description = request.POST.get('request_description')
        
        # req_from= request.POST.get('req_from')
        inquiry = Inquiry(user_name= user_name, email= email, contact=contact, venue_name=venue_name, request_description=request_description )

        inquiry.save()

# send send_mail
        send_mail(
            'Venue Cate',
            'Hi ' + user_name + ', \n\nThank you for contacting us, Our team will get back soon to your request on ' + user_name + ' with your preferred choice \n\nPACKAGE : ' + user_name + ' \nPLAN : ' + user_name + '.' ,
            'venuecate2211@gmail.com',
            recipient_list=[email],
            html_message ='''<div><div></div><div tabindex="-1"></div><div><div><u></u><div style="margin:0!important;padding:0!important"> <img style="display:none!important"><table border="0" cellpadding="0" cellspacing="0" width="100%"><tbody><tr><td width="100%" align="center" valign="top" bgcolor="#eeeeee" height="20"></td></tr><tr><td bgcolor="#eeeeee" align="center" style="padding:0px 15px 0px 15px"><table bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px"><tbody><tr><td><table width="100%" border="0" cellspacing="0" cellpadding="0"><tbody><tr><td align="center" style="padding:40px 40px 0px 40px"> <a href="#" target="_blank" data-saferedirecturl="#"> <img src="https://Venue Cate.herokuapp.com/static/media/logo1.png" alt="Venue Cate logo" width="auto" border="0" style="vertical-align:middle"> </a></td></tr><tr><td align="center" style="font-size:18px;color:#0e0e0f;font-weight:700;font-family:Helvetica Neue;line-height:28px;vertical-align:top;text-align:center;padding:35px 40px 0px 40px"> <strong>'''+ venue_name + ''' </strong></td></tr><tr><td align="center" bgcolor="#ffffff" height="1" style="padding:40px 40px 5px" valign="top" width="100%"><table cellpadding="0" cellspacing="0" width="100%"><tbody><tr><td style="border-top:1px solid #e4e4e4"> <br> <br>Hi ''' + user_name + ''', <br> <br>Thank you for contacting us, Our team will get back soon to your request. <br>Your preferred choices are: <br> <br>PACKAGE : ''' + venue_name +''' <br>PLAN : ''' + user_name + ''' <br> <br> <strong>Regards <br> Venue Cate </strong></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td width="100%" align="center" valign="top" bgcolor="#ffffff" height="45"></td></tr></tbody></table></td></tr><tr><td bgcolor="#eeeeee" align="center" style="padding:20px 0px"><table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" style="max-width:600px"><tbody><tr></tr><tr><td bgcolor="#eeeeee" align="center"><table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" style="max-width:600px"><tbody><tr><td align="center" style="text-align:center;padding:10px 10px 10px 10px"><p>&#169;copyright @ 2020 Venue Cate</p></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><div></div><div></div></div><div></div></div></div><div style="display:none"><div></div></div><div></div></div>''' ,
            fail_silently=False
        )
        
        messages.success(request,'Your message has been sucessfully sent, Please check your E-mail.')
        
        return render(request, 'accounts/vendorRequest.html')


def inquiryinfo(request):
    inq = Inquiry.objects.all()
    print("Myoutput",inq)
    return render(request,'accounts/adminDashboard.html',{'inqu': inq})


def feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        feedback = request.POST['feedback']
        
        feedback = Feedback(name=name, email=email, feedback=feedback)

        feedback.save()

        # send send_mail
        # send send_mail
        
        
        # return HttpResponseRedirect('/admin')
    return render(request, 'accounts/index.html')

# function to add venue
# def add_venue(request):
#     if request.method=='GET':
#         form = add_venueForm()
#         return render(request,'accounts/add_venue.html',{'form':form})
#     else:
#         form = add_venueForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('/add_venue/')
         
    # else:
    #     form  = add_venueForm()
    # return render(request,'accounts/add_venue.html',{'form' : form})

def venue(request):

    venue_form = venueForm()
    venueImage_form = venueImageForm()
    extraService_form = extraServiceForm()
    if request.method == 'POST':  
        # form fields
        extra_service_fields = ['serviceName']
        venue_fields = ['venueName','image', 'address', 'district', 'min_guestCapacity', 'max_guestCapacity', 'price', 'contact', 'description', 'website', 'openTime', 'closingTime']
        venue_image_fields = ['images']
        
        print("post data", request.POST, type(request.POST))

        # for extras
        extras_inputs = {}
        for key in extra_service_fields:
            extras_inputs[key] = request.POST.get(key)
        print("extras inputs", extras_inputs, type(extras_inputs))
        query_dict1 = QueryDict('', mutable=True)
        query_dict1.update(extras_inputs)
        extraService_form = extraServiceForm(**query_dict1)
        # print("extras form", extraService_form)

        # for venue image
        venue_image = {}
        for key in venue_image_fields:
            venue_image[key] = request.POST.get(key)
        query_dict2 = QueryDict('', mutable=True)
        query_dict2.update(venue_image)
        venueImage_form = venueImageForm(**query_dict2)
        # print("image form", venueImage_form)

        # for venue
        venue = {}
        for key in venue_fields:
            venue[key] = request.POST.get(key)
        query_dict3 = QueryDict('', mutable=True)
        query_dict3.update(venue)
        venue_form = venueForm(**query_dict3)
        # print("venue form", venue_form)
                
        print("request data", request.POST)
        # print("venue image errors", venueImage_form.errors)
        # print("venue extra service form errors", extraService_form.errors)
        # print("venue form errors", venue_form.errors)

        if venue_form.is_valid() and extraService_form.is_valid() and venueImage_form.is_valid():

            venue.save()
            extraService=extraService_form.save(commit=False)
            extraService.venue = venue
            extraService.save()
            venueImage = veneuImage_form.save(commit= False)
            veneuImage.venue = venue
            venueImage.save()
            print(venue)

    context = {'venue_form':venue_form, 'extraService_form':extraService_form, 'venueImage_form':venueImage_form,}
    return render(request, "accounts/venue.html", context)

    # if request.method=='POST':
    #    venue_form = venueForm(request.POST)
    #    extraService_form = extraServiceForm(request.POST)
    #    venueImage_form = venueImageForm(request.POST)
       
    #    if venue_form.is_valid() and extraServiceForm.is_valid() and venue_form.is_valid():
    #        venue= venue_form.save(commit=False)
    #        extraService= extraService_form.save(commit=False)
    #        extraService.venue = venue
    #        venue.save()
    #        venueImage= venueImage_form.save()
    #        venueImage.venue= venue
    #        venue.save()
    
    # venue_form= forms.venueForm()
    # extraService_form= forms.extraServiceForm()
    # venueImage_form= forms.venueImageForm()

    # context= {'venue_form':venue_form, 'extraService_form':extraService_form, 'venueImage_form':venueImage_form}
    # return render(request, 'accounts/venue.html')






    # if request.method == 'GET':
    #     form = venueForm()
    #     return render(request,"accounts/venue.html",{'form':form})
    # else:
    #     form = venueForm(data = request.POST)
    #     print(request.POST)
    #     if form.is_valid():
    #         print("form valid-----")
    #         form.save()
    #     else:
    #         print("Form invalid---------------")
        # return redirect('/accounts/venue.html/')

    # if request.method == 'POST':
    #     print(request.POST)
    #     form  =  venueForm(request.POST)
    #     if form.is_valid():
    #         add = form.save(commit=False)
    #         add.venueName= request.POST.get('venueName')
    #         add.address=request.POST.get('address')
    #         add.district=request.POST.get('district')
    #         add.min_guestCapacity= request.POST.get('min_guestCapacity')
    #         add.max_guestCapacity= request.POST.get('max_guestCapacity')
    #         add.price= request.POST.get('price')
    #         add.contact=request.POST.get('contact')
    #         add.description= request.POST.get('description')
    #         add.website=request.POST.get('website')
    #         add.addService= request.POST.get('addService')
    #         add.openTime= request.POST.get('openTime')
    #         add.closingTime= request.POST.get('closingTime')
    #         # add.addService= request.POST.get('addService')
    #         # addService= AddService.objects.create(
    #         #     'serviceName':serviceName,
    #         #     'servicePrice':servicePrice,
    #         # )
    #         # addService.save()
            
    #         add.save()
    #         return HttpResponse('/Venue is added successfully/')
    # else:
    #     form = venueForm()
    # return render(request, 'accounts/venue.html', {'form':form})


       
    


# def cateirng(request):
#     if request.method =='POST':
#         form= cateringForm(request.POST)
#         if form.is_valid():
#             catering = form.cleaned_data.get('catering')
#     else:
#         form = cateirng
#     return render('accounts/bookingForm.html', {'form': form})     #render_to_response

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

def userTable(request):
    profile = Profile.objects.all()
    return render(request,'accounts/userTable.html', {'profile':profile})
   
def bookingTable(request):
    booking= Booking.objects.all()
    return render(request,'accounts/bookingTable.html' ,{'booking':booking})

def venueTable(request):
    venue = Venue.objects.all()
    return render(request,'accounts/venueTable.html', {'venue':venue} )


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

def payment(request):
    return render(request, "accounts/payment.html")



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


# venue api created newly
class VenueView(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


# ashutosh 
class InquiryView(viewsets.ModelViewSet):
    queryset= Inquiry.objects.all()
    serializer_class = InquirySerializer



class VendorRequestViewset(viewsets.ModelViewSet):
    queryset = VendorRequest.objects.all()
    serializer_class = VendorRequestSerializer
