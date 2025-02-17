from django.contrib import admin
from django.urls import path,include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('cars/', include('apps.listings.urls')),
    path('users/', include('apps.users.urls')),
    
]