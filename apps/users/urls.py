from django.contrib import admin
from django.urls import path
from .views import register,login_view,logout_view,dashboard_view,toggle_annonce
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('singup/', register, name='register'),
    path('login/', login_view , name='login'),
    path("logout/", logout_view, name="logout"),

    path('hote/',dashboard_view,name='dashboard'),
    path("toggle-annonce/<int:car_id>/", toggle_annonce, name="toggle_annonce"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
