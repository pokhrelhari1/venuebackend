
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Profile, Booking

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
        fields= [ 'guestNumber' ,'eventStartDate','eventEndDate','eventType','catering', 'extraService']




  

