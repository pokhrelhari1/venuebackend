from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import FieldDoesNotExist
from django import forms

# model for userdetail.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, help_text='Email')
    address = models.CharField(max_length=150)
    contact = models.IntegerField(null= True, blank= True )
    profile_picture = models.ImageField(upload_to = 'accounts/static/images/')
   

    def __str__(self):
        return self.first_name

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Category(models.Model):
    name= models.CharField(max_length=100)


    def __str__(self):
        return self.name

    
class Menu_Items(models.Model):
    name= models.CharField(max_length= 100)
    category = models.ManyToManyField('Category', related_name='item')
    
    def __str__(self):
        return self.name

class food_Package(models.Model):
    packageName= models.CharField(max_length= 100)
    price = models.IntegerField(null="False", blank= False)
    Menu_Items = models.ManyToManyField('Menu_Items', related_name='Menu_Items')

    def __str__(self):
        return self.packageName


class OrderedFoodPackage(models.Model):
    packageName= models.CharField(max_length= 100)
    price = models.IntegerField(null="False", blank= False)
    Menu_Items = models.ManyToManyField('Menu_Items')

    def __str__(self):
        return self.packageName



#model for catering  
class Catering(models.Model):
    created_on= models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(null=True, blank=False) 
    packageType = models.ManyToManyField('food_Package', related_name='food_Package' ,blank=False)


    def __str__(self):
        return f'Catering:{self.created_on.strftime("%b %d %I: %M %p")}'
   
    # def __str__(self):
    #     return self.items


   
#model for extra sevice
class extraService(models.Model):
    serviceName= models.CharField(max_length= 200, blank=True)
    servicePrice= models.IntegerField(null=True, blank= True)
    catering= models.ForeignKey(Catering, on_delete= models.SET_NULL, blank= True, null=True)

    
    def __str__(self):
        return self.serviceName


# model for venue details
class Venue(models.Model):
    venueName= models.CharField(max_length= 100, blank=True )
    image= models.ImageField(upload_to = 'images/')
    address= models.CharField(max_length= 100, blank=True )
    district = models.CharField(max_length = 50, blank = True, null = True)
    min_guestCapacity= models.IntegerField(null= True, blank= True )
    max_guestCapacity= models.IntegerField(null= True, blank= True )
    price = models.IntegerField(null= True, blank= True )
    contact = models.IntegerField(null= True, blank= True )
    description = models.CharField(max_length= 1000, blank=True )
    website = models.URLField(max_length= 1000, blank=True )
    openTime = models.TimeField(null=True, blank=True)
    closingTime = models.TimeField(null=True, blank=True)
    addService= models.ManyToManyField(extraService)
    #many to many  
    
        
    def descriptionSummery(self):
        return self.description
    
    def __str__(self):
        return self.venueName



class Inquiry(models.Model):
    user_name= models.CharField(max_length=50, null= True, blank= True )
    email = models.CharField(max_length = 20, blank = True, null = True)
    contact = models.IntegerField(null= True, blank= True )
    venue_name = models.CharField(max_length = 100, null = True, blank = True)
    request_description = models.CharField(max_length = 500, null = True, blank = True)
    
    
    # req_from = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    
        
    def descriptionSummery(self):
        return self.description
    
    def __str__(self):
        return self.venueName




# class Inquiry(models.Model):
#     venueName= models.CharField(max_length= 100, blank=True )
#     address= models.CharField(max_length= 100, blank=True )
#     district = models.CharField(max_length = 50, blank = True, null = True)
#     email = models.CharField(max_length = 1000, blank = True, null = True)
#     contact = models.IntegerField(null= True, blank= True )
#     description = models.CharField(max_length= 1000, blank=True )
    
        
#     def descriptionSummery(self):
#         return self.description
    
#     def __str__(self):
#         return self.venueName

#model for multiple image 
class venueImage(models.Model):
    venue = models.ForeignKey(Venue, default=None, on_delete=models.SET_NULL, null = True)
    images= models.FileField(upload_to='images/')

    def __str__(self):
        return self.venue.venueName



# model for booking 

class Booking(models.Model):
   
    bookingdate = models.DateField(auto_now_add=True)
    guestNumber = models.IntegerField(blank=True)
    eventStartDate= models.DateField(auto_now_add=False)
    # eventEndDate= models.DateField(auto_now_add=False)
    eventType= models.CharField(max_length=500, blank=True)
    venue= models.ForeignKey(Venue, on_delete=models.CASCADE)
    # catering= models.ForeignKey(Catering, on_delete= models.CASCADE, null=True)                
    customer= models.ForeignKey(Profile,on_delete= models.CASCADE)
    extraService= models.ForeignKey(extraService, null = True, on_delete= models.CASCADE)
    foodpackage = models.ForeignKey(OrderedFoodPackage, on_delete=models.CASCADE, null=True)    #change null=False

    
     
#model for payment 
# class Payment(models.Model):
#     paymentDate= models.DateTimeField(default=datetime.now(), blank=True)
#     amount= models.IntegerField(null=True, blank=True)
#     booking= models.ForeignKey(Booking, on_delete= models.CASCADE)

class Payment(models.Model):
    paymentDate= models.DateTimeField(default=datetime.now(), blank=True)
    amount= models.IntegerField(null=True, blank=True)
    booking= models.ForeignKey(Booking, on_delete= models.CASCADE)


#model for feedback 
class Feedback(models.Model):
    name=models.CharField(max_length=1000, blank=True)
    email= models.CharField(max_length=1000, blank=True)
    feedback= models.CharField(max_length=1000, blank=True)
   
   

  
#     def __str__(self):
#         return self.foodItems

# #model for catering service

# class Catering(models.Model):
#     menu = models.ForeignKey(Menu, default=None, on_delete=models.CASCADE)
#     price =IntegerField( null= True, blank=True)
    
#     def __str__(self):
#         return self.fooditems


# #model for service table
# class Service(models. Model):
#     venue = models.ForeignKey(Venue, default=None, on_delete=models.CASCADE)
#     catering = models.ForeignKey(Catering, default=None, on_delete=models.CASCADE)
#     totalPrice= models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return self.Service.I

class VendorRequest(models.Model):
    venue_name = models.CharField(max_length = 100, null = True, blank = True)
    request_description = models.CharField(max_length = 500, null = True, blank = True)
    email = models.CharField(max_length = 20, blank = True, null = True)
    req_from = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    user_name= models.CharField(max_length=50, null= True, blank= True )
    is_accepted = models.BooleanField(default = False)