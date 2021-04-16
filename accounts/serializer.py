from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'url','first_name', 'last_name', 'email', 'address', 'contact','profile_picture']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue 
        lookup_fileds = ('price','max_guestCapacity')
        fields = ['id', 'url','venueName','image', 'address', 'district','min_guestCapacity','max_guestCapacity','price', 'contact','description', 'website', 'openTime','closingTime','addService' ]

# ashutosh 
class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry 
    
        fields = ['id', 'venueName', 'address', 'district', 'email', 'contact','description', ]


class venueImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = venueImage
        fields = ['url', 'venue', 'images']


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
        fields= ['packageType','created_on','price']            


class food_PackageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= food_Package
        lookup_filed = 'packageName'
        fields= ['packageName','price','Menu_Items']


    
class Menu_ItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Menu_Items
        lookup_filed = 'name'
        fields= ['name','category']

    
class CatogerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Category
        lookup_filed = 'name'
        fields= ['name']
        

class extraServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= extraService
        lookup_filed='serviceName'
        fields = ['serviceName', 'servicePrice','catering']


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields= ['bookingdate', 'eventStartDate', 'eventType', 'venue', 'catering', 'customer']

class VendorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRequest
        fields = '__all__'