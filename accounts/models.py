from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime


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


    


#model for catering
class Catering(models.Model):
    foodType= models.CharField(max_length=200, blank= True)
    foodItems= models.CharField(max_length=200, blank= True)
    is_available=models.BooleanField( null= False, blank= False)
    price= models.IntegerField(null= True, blank= True)


    def __str__(self):
        return self.foodType

   

#model for extra sevice
class extraService(models.Model):
    serviceName= models.CharField(max_length= 200, blank=True)
    servicePrice= models.IntegerField(null=False, blank= False)
    catering= models.ForeignKey(Catering, on_delete= models.CASCADE)

# model for venue details
class Venue(models.Model):
    venueName= models.CharField(max_length= 100, blank=True )
    image= models.ImageField(upload_to = 'images/')
    address= models.CharField(max_length= 100, blank=True )
    min_guestCapacity= models.IntegerField(null= True, blank= True )
    max_guestCapacity= models.IntegerField(null= True, blank= True )
    price = models.IntegerField(null= True, blank= True )
    contact = models.IntegerField(null= True, blank= True )
    description = models.CharField(max_length= 1000, blank=True )
    website = models.URLField(max_length= 1000, blank=True )
    openTime = models.TimeField(null=True, blank=True)
    closingTime = models.TimeField(null=True, blank=True)
    addService= models.ForeignKey(extraService, on_delete= models.CASCADE)
    

    def descriptionSummery(self):
        return self.description
    
    def __str__(self):
        return self.venueName

#model for multiple image 
class venueImage(models.Model):
    venue = models.ForeignKey(Venue, default=None, on_delete=models.CASCADE)
    images= models.FileField(upload_to='images/')

    def __str__(self):
        return self.venue.venueName



# model for booking 
class Booking(models.Model):
    bookingdate = models.DateTimeField(default=datetime.now(), blank=True)
    eventStartDate= models.DateTimeField(auto_now_add=False)
    eventEndDate= models.DateTimeField(auto_now_add=False)
    eventType= models.CharField(max_length=500, blank=True)
    venue= models.ForeignKey(Venue, on_delete=models.CASCADE)
    catering= models.ForeignKey(Catering, on_delete= models.CASCADE)
    customer= models.ForeignKey(Profile,on_delete= models.CASCADE)

    
     
#model for payment 
class Payment(models.Model):
    paymentDate= models.DateTimeField(default=datetime.now(), blank=True)
    amount= models.IntegerField(null=True, blank=True)
    booking= models.ForeignKey(Booking, on_delete= models.CASCADE)


#model for feedback 
class Feedback(models.Model):
    feedback=models.CharField(max_length=1000, blank=True)
    feedbackDate= models.DateTimeField(default=datetime.now(), blank=True)
    customer= models.ForeignKey(Profile, on_delete= models.CASCADE)

    
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
    