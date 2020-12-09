
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserFrom(UserCreationForm): #replica of default form
    first_name= forms.CharField(max_length= 100, help_text="First Name")
    last_name= forms.CharField(max_length= 100, help_text="First Name")
    email = forms.EmailField(max_length=150, help_text='Email')
    address= forms.CharField(max_length= 100, help_text="Address")
    contact= forms.IntegerField(required=True) 

    class Meta:
        model = User
        fields= ['username','first_name', 'last_name', 'email','address', 'contact','password1','password2' ]
