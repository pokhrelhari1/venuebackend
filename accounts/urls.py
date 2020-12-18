from django.urls import path
from .import views



urlpatterns = [
    path ('register/', views.registerPage, name='register'),
    path ('login/', views.loginPage, name='login'),
    path ('logout/', views.logoutUser, name='logout'),
    path('',views.index, name='index'),
    path('viewDetail/',views.viewDetail, name='viewDetails'),
    path('customer/',views.customer),
    path('dashboard/',views.dashboard, name= 'dashboard'),
]