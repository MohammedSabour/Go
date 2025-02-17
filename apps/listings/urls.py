from django.urls import path
from .views import search_cars, check_car, CarAnnonceWizard
from django.conf import settings
from django.conf.urls.static import static
from .forms import LocationForm, CarModelForm, DispoForm, CarModelDetailsForm, DescriptionForm, CarImageForm


urlpatterns = [
    path('rechercher/', search_cars, name='search_cars'),
    path('check-car/', check_car, name='check_car'),
    path('inscription/',CarAnnonceWizard.as_view([LocationForm, CarModelForm, CarModelDetailsForm, DispoForm, DescriptionForm, CarImageForm]),name='hote'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
