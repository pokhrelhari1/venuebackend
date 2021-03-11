
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from djnago.contrib.auth.models import User
# from rest_framework import routers, serializers, viewsets



urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', include('accounts.urls')),
    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)