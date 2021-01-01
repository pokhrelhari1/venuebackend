from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path ('register/', views.registerPage, name='register'),
    path ('login/', views.loginPage, name='login'),
    path ('logout/', views.logoutUser, name='logout'),
    path('',views.index, name='index'),
    path('user/',views.user, name='user'),
    path('viewDetail/<str:id>/',views.viewDetail, name='viewDetail'),
  
    # path('venue/id/', views.viewDetails, name='viewDetails'),
    path('customer/',views.customer),
    path('dashboard/',views.dashboard, name= 'dashboard'),
    path ('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path ('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),  name="password_reset_done") ,    #render success message to  notify user to cheeck their email
    path ('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name= "password_reset_confirm"),     
    path ('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),  name="password_reset_complete"),


]
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)