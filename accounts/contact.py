from django import forms

class ContactForm(forms.Form):
    user_name=forms.CharField(max_length=1000, blank=True)
    email= forms.CharField(max_length=1000, blank=True)
    message=forms.CharField(max_length=1000, blank=True)
   
   

