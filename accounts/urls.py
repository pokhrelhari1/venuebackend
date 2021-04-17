from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .import views
from django.conf.urls import url


# api route
router = routers.DefaultRouter()
router.register('accounts', views.VenueView)

router.register('catering', views.CateringView)
router.register('feedback', views.FeedbackView)
router.register('venueImage', views.venueImageView)
router.register('profile', views.ProfileView, basename="profile")
router.register('booking', views.BookingView)
router.register('payment', views.PaymentView)
router.register('food_package', views.food_PackageView)
router.register('Menu_Items', views.Menu_ItemsView)
router.register('Catogery', views.CategoryView)


#  venue api created newly
router.register('venues', views.VenueView)

#inquriy api
router.register('inquiry', views.InquiryView)

router.register('vendor-request', views.VendorRequestViewset)


urlpatterns = [
    path ('register/', views.registerPage, name='register'),
    path ('login/', views.loginPage, name='login'),
    path ('inquirys/', views.inquiry, name='inquirys'),
    path ('logout/', views.logoutUser, name='logout'),
    path('',views.index, name='index'),
    
    path('<int:id>/bookingForm/', views.booking, name= 'bookingForm'),
    path ('catering/<int:id>/', views.catering.as_view(), name= 'catering'),
    path('foodpackage/<int:id>/', views.food_package_menu, name='foodpackage'),
    # path ('searchbar', views.searchbar, name='searchbar'),

    # url(r'^search/$', views.searchbar, name='searchbar'),

  
    path('userProfile/',views.userProfile, name='userProfile'),
    path('userTable/',views.userTable, name='userTable'),
    path('venueTable/',views.venueTable, name='venueTable'),
    path('bookingTable/',views.bookingTable, name='bookingTable'),
    # path('contact/', contact, name='contact'),
    path('feedback/',views.feedback, name='feedback'),
    path('payment/',views.payment, name='payment'),
    
    path('venue/',views.venue, name='venue'),
    path('updateProfile',views.updateProfile, name='updateProfile'),
    path('searchbar',views.searchbar, name='searchbar'),
    path('viewDetail/<str:id>/',views.viewDetail, name='viewDetail'),
    path('tables/',views.tables, name='tables'),
    path('<int:id>/deleteBooking/',views.deleteBooking, name='deleteBooking'),
    path('deleteVenue/<str:id>/',views.deleteVenue, name='deleteVenue'),
   
    #  url(r'^search/$', views.search, name='search'),

    # path('venue/id/', views.viewDetails, name='viewDetails'),
    
    path('adminDashboard/',views.adminDashboard, name= 'adminDashboard'),
    path('userDashboard/',views.userDashboard, name= 'userDashboard'),
    path('vendorRequest/',views.vendorRequest, name= 'vendorRequest'),
    path('inquirys/',views.vendorRequest, name= 'inquirys'),
    path ('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path ('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),  name="password_reset_done") ,    #render success message to  notify user to cheeck their email
    path ('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name= "password_reset_confirm"),     
    path ('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),  name="password_reset_complete"),

    path ('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path ('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path ('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_view"),
    path ('reset_password_complete/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_complete"),
    path('editVenue/<int:id>/', views.editVenue, name="editVenue"),

    path('searchLocation', views.searchLocation),
    path('filter_venue/', views.filter_venue, name="filter_venue"),

     path('', include(router.urls)),


     path('viewBookingDetails/', views.viewBookingDetails, name="viewBookingDetails")




]
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
