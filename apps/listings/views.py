from django.shortcuts import get_object_or_404,render,redirect

from formtools.wizard.views import SessionWizardView
from django.contrib.auth.decorators import login_required
from .forms import LocationForm, CarModelForm, CarModelDetailsForm, DispoForm, DescriptionForm, CarImageForm
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Car,Annonce,CarImage
from apps.reservations.models import Reservation
from django.core.files.storage import FileSystemStorage
from django.db import transaction
import logging
import requests

logger = logging.getLogger(__name__)

def search_cars(request):
    location = request.GET.get('location', '').strip()
    start_date_str = request.GET.get('start_date', '').strip()
    end_date_str = request.GET.get('end_date', '').strip()

    min_price = request.GET.get('min_price', '2500')
    max_price = request.GET.get('max_price', '25000')

    context = {
        'error': None,
        'available_cars': [],
        'locations': [],
        'min_price': min_price,
        'max_price': max_price
    }

    if not location or not start_date_str or not end_date_str:
        context['error'] = "Veuillez fournir la localisation, la date de début et la date de fin."
        return render(request, 'search_results.html', context)

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        min_price = float(min_price)
        max_price = float(max_price)
    except ValueError:
        context['error'] = "Format invalide pour les dates ou les prix."
        return render(request, 'search_results.html', context)

    if start_date > end_date:
        context['error'] = "La date de début doit être avant la date de fin."
        return render(request, 'search_results.html', context)

    try:
        # Récupération des voitures disponibles
        cars = Car.objects.filter(
            location__icontains=location,
            status=Car.APPROVED,
            annonce__is_active=True,
            annonce__price_per_day__gte=min_price,
            annonce__price_per_day__lte=max_price
        ).prefetch_related('annonce__images')

        if not cars.exists():
            context['error'] = "Aucune voiture trouvée pour cet emplacement"
            return render(request, 'search_results.html', context)

        # Exclure les voitures déjà réservées
        unavailable_cars = Reservation.objects.filter(
            status__in=[Reservation.ACCEPTED, Reservation.PAID, Reservation.ONGOING],
            start_date__lte=end_date,
            end_date__gte=start_date
        ).values_list('car_id', flat=True)

        available_cars = cars.exclude(id__in=unavailable_cars)

        # 🔹 Application des filtres supplémentaires
        brand = request.GET.get("brand", "").strip()
        year = request.GET.get("year", "").strip()
        seats = request.GET.get("seats", "").strip()

        if brand:
            available_cars = available_cars.filter(brand__iexact=brand)
        if year.isdigit():  # Vérification pour éviter une erreur
            available_cars = available_cars.filter(year=int(year))
        if seats.isdigit():
            available_cars = available_cars.filter(seats=int(seats))

        if not available_cars.exists():
            context['error'] = "Aucune voiture disponible avec ces filtres."

        # Ajouter les voitures disponibles au contexte
        context['available_cars'] = available_cars

    except Exception as e:
        logger.error(f"Erreur lors de la recherche des voitures : {e}")
        context['error'] = "Une erreur est survenue lors de la recherche des voitures. Veuillez réessayer."

    return render(request, 'search_results.html', context)

@login_required
def check_car(request):
    """Vérifie si l'utilisateur a déjà une voiture et redirige en conséquence."""
    if Car.objects.filter(owner=request.user).exists():
        return redirect('dashboard')
    return redirect('hote')


class CarAnnonceWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [LocationForm, CarModelForm, CarModelDetailsForm, DispoForm, DescriptionForm, CarImageForm]
    template_name = "hote.html"
    file_storage = FileSystemStorage()

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        current_step = int(self.steps.current) if self.steps.current.isdigit() else 0
        context['progress_percentage'] = int((current_step + 1) / len(self.form_list) * 100)
        return context

    def get_form_initial(self, step):
        """ Pré-remplit les formulaires si une voiture existe déjà """
        car_id = self.request.GET.get('car_id')
        if car_id:
            car = get_object_or_404(Car, id=car_id, owner=self.request.user)
            annonce = getattr(car, 'annonce', None)

            initial_data = {
                "0": {"location": car.location, "latitude": car.latitude, "longitude": car.longitude},
                "1": {"brand": car.brand, "model": car.model, "year": car.year},
                "2": {"transmission": car.transmission, "fuel_type": car.fuel_type, "seats": car.seats},
                "3": {"duree_minimale": annonce.duree_minimale if annonce else None, "duree_maximale": annonce.duree_maximale if annonce else None},
                "4": {"price_per_day": annonce.price_per_day if annonce else None, "description": annonce.description if annonce else None},
            }

            return initial_data.get(step, {})

        return super().get_form_initial(step)

    def done(self, form_list, **kwargs):
        user = self.request.user
        car_id = self.request.GET.get('car_id')
        
        if not all(form.is_valid() for form in form_list):
            return self.render_revalidation_failure(form_list)

        location_data = form_list[0].cleaned_data
        car_model_data = form_list[1].cleaned_data
        car_model_details_data = form_list[2].cleaned_data
        dispo_data = form_list[3].cleaned_data
        description_data = form_list[4].cleaned_data
        car_images_form = form_list[5]

        with transaction.atomic():
            if car_id:
                # Modification d'une voiture existante
                car = get_object_or_404(Car, id=car_id, owner=user)
                for field, value in {**location_data, **car_model_data, **car_model_details_data}.items():
                    setattr(car, field, value)
                car.save()
                
                annonce = getattr(car, 'annonce', None)
                if annonce:
                    for field, value in {**dispo_data, **description_data}.items():
                        setattr(annonce, field, value)
                    annonce.save()
                else:
                    annonce = Annonce.objects.create(car=car, **dispo_data, **description_data)
            else:
                car = Car.objects.create(
                    location=location_data['location'],
                    latitude=location_data['latitude'],
                    longitude=location_data['longitude'],
                    owner=user,
                    **car_model_data,
                    **car_model_details_data
                )
                annonce = Annonce.objects.create(car=car, **dispo_data, **description_data)

            # Gestion des images
            car_images = car_images_form.cleaned_data.get('image')
            if car_images:
                for img in car_images:
                    CarImage.objects.create(annonce=annonce, image=img)

        return redirect('dashboard')

    def render_revalidation_failure(self, form_list):
        return self.render(self.request, self.template_name, {
            'form_list': form_list,
            'errors': [form.errors for form in form_list],
        })