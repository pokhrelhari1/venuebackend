from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'url','first_name', 'last_name', 'email', 'address', 'contact','profile_picture']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue 
        fields = ['id', 'url','venueName','image', 'address','min_guestCapacity','max_guestCapacity','price', 'contact','description', 'website', 'openTime','closingTime','addService' ]


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields= ['bookingdate', 'url','eventStartDate', 'eventEndDate','eventType','venue','catering','customer']


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Feedback
        fields= ['feedback', 'url','feedbackDate','customer']
 
class CateringSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Catering
        fields= ['foodType','url','foodItems', 'is_available','price']
        

class extraServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= extraService
        lookup_filed='serviceName'
        fields = ['serviceName', 'servicePrice','catering']


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields= ['bookingdate', 'eventStartDate', 'eventEndDate', 'eventType', 'venue', 'catering', 'customer']