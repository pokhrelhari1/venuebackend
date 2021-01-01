from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

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

# model for venue details
class Venue(models.Model):
    venueName= models.CharField(max_length= 100, blank=True )
    image= models.ImageField(upload_to = 'images/')
    address= models.CharField(max_length= 100, blank=True )
    contact = models.IntegerField(null= True, blank= True )
   
    description = models.CharField(max_length= 500, blank=True )
    openTime = models.TimeField()
    closingTime = models.TimeField()
    
    def __str__(self):
        return self.venueName

#model for multiple image 
class venueImage(models.Model):
    venue = models.ForeignKey(Venue, default=None, on_delete=models.CASCADE)
    images= models.FileField(upload_to='images/')

    def __str__(self):
        return self.venue.venueName