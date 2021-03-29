from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .import views



router = routers.DefaultRouter()
router.register('accounts', views.VenueView)
router.register('catering', views.CateringView)
router.register('feedback', views.FeedbackView)
router.register('profile', views.ProfileView, basename="profile")
router.register('booking', views.BookingView)
router.register('payment', views.PaymentView)


urlpatterns = [
    path ('register/', views.registerPage, name='register'),
    path ('login/', views.loginPage, name='login'),
    path ('logout/', views.logoutUser, name='logout'),
    path('',views.index, name='index'),
    
    path('<int:id>/bookingForm/', views.booking, name= 'bookingForm'),
    path ('catering/<int:id>', views.catering.as_view(), name= 'catering'),
   
    path('userProfile/',views.userProfile, name='userProfile'),
    path('updateProfile',views.updateProfile, name='updateProfile'),
    path('viewDetail/<str:id>/',views.viewDetail, name='viewDetail'),
    path('<int:id>/deleteBooking/',views.deleteBooking, name='deleteBooking'),
   

    # path('venue/id/', views.viewDetails, name='viewDetails'),
    path('dashboard/',views.dashboard, name= 'dashboard'),
    path ('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path ('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),  name="password_reset_done") ,    #render success message to  notify user to cheeck their email
    path ('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name= "password_reset_confirm"),     
    path ('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),  name="password_reset_complete"),

    path ('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path ('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path ('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_view"),
    path ('reset_password_complete/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_complete"),


     path('', include(router.urls))






]
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)