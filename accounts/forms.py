
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Profile, Booking, Venue, extraService, venueImage
from django.db import models

class CreateUserFrom(UserCreationForm): #replica of default form
    username= forms.CharField(max_length= 100, help_text="First Name")
    first_name= forms.CharField(max_length= 100, help_text="First Name")
    last_name= forms.CharField(max_length= 100, help_text="First Name")
    email = forms.EmailField(max_length=150, help_text='Email')
    address= forms.CharField(max_length= 100, help_text="Address")
    contact= forms.IntegerField() 

    class Meta:
        model = User
        fields= ['username','first_name', 'last_name', 'email','address', 'contact','password1','password2' ]
       

class CustomerForm(ModelForm):
    class Meta:
        model = Profile
        fields= ['first_name', 'last_name', 'email','address', 'contact','profile_picture']


class bookingForm(ModelForm):
    class Meta:
        model = Booking
        fields= [ 'guestNumber' ,'eventStartDate','eventType', 'extraService', 'totalPrice']


class cateringForm(forms.Form):
    OPTIONS=(
        ("package1"),

    )

    
    catering = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)

class venueForm(forms.ModelForm):
    class Meta:
        model = Venue
        # fields=['venueName','image', 'address', 'district', 'min_guestCapacity', 'max_guestCapacity', 'price', 'contact', 'description', 'website', 'openTime', 'closingTime']
        fields = '__all__'


class extraServiceForm(forms.ModelForm):
    class Meta:
        model = extraService
        fields=['serviceName']

class venueImageForm(forms.ModelForm):
    class Meta:
        model =venueImage
        fields=['images']
  
# class venueForm(forms.ModelForm):
#     class Meta:
#         model = Venue
#         fields=['venueName', 'address','district','image' ,'min_guestCapacity' ,'max_guestCapacity', 'price', 'contact', 'description', 'website', 'openTime',
# 'closingTime', 'addService']
        
    
#     # def __init__(self, *args, **kwargs):
#     #     super(venueForm,self),__init__(*args, **kwargs)
#     #     self.fields['extraService'].empty_label= "Select"

# class extraServiceForm(ModelForm):
#     class Meta:
#         model:extraService
#         fields=['serviceName', 'servicePrice']

# class venueImageForm(ModelForm):
#     class Meta:
#         model: venueImage
#         fileds=['images']  