from django.contrib import admin
from .models import Profile
from .models import Venue, venueImage, extraService

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