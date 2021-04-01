from django.contrib import admin
from .models import Profile
from .models import Venue, venueImage, extraService, Booking, Payment, Catering, Feedback, Menu_Items, Category, food_Package, OrderedFoodPackage

admin.site.register(Profile)

#configuring single admin for different model
class venueImageAdmin(admin.StackedInline):
    model= venueImage

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    inlines = [venueImageAdmin]

    class Meta:
        model= Venue

@admin.register(venueImage)
class venueImageAdmin(admin.ModelAdmin):
    pass


@admin.register(extraService)
class extraServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    pass

@admin.register(Catering)
class CateringAdmin(admin.ModelAdmin):
    pass

@admin.register(Menu_Items)
class MenuItemsAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(food_Package)
class food_PackageAdmin(admin.ModelAdmin):
    pass



admin.site.register(OrderedFoodPackage)