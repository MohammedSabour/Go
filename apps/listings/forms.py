from django import forms
from .models import Car,Annonce,CarImage
from datetime import datetime
from django.core.exceptions import ValidationError
import requests

# Étape 1 : Localisation
class LocationForm(forms.ModelForm):
    location = forms.CharField(
        label="Emplacement de la voiture",
        widget=forms.TextInput(attrs={
            "id": "locationCar",
            "placeholder": "Saisissez une adresse",
            "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200 transition-shadow",
        }),
        error_messages={"required": "Ce champ est obligatoire."},
    )

    class Meta:
        model = Car
        fields = ["location", 'latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(attrs={
                "id": "latitude",
            }),
            'longitude': forms.HiddenInput(attrs={
                "id": "longitude",
            }),
        }

    def clean_location(self):
        location = self.cleaned_data.get("location")

        if not location:
            raise ValidationError("Ce champ est obligatoire.")

        # Appel à l'API de géocodage pour vérifier le pays
        url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
        response = requests.get(url, headers={'User-Agent': 'DjangoApp'})
        
        if response.status_code == 200 and response.json():
            data = response.json()[0]  # Prendre le premier résultat
            country = data.get("display_name", "").lower()

            if "algérie" not in country and "algeria" not in country:
                raise ValidationError("Demande non valide.")

        else:
            raise ValidationError("Impossible de valider cette adresse. Vérifiez qu'elle est correcte.")

        return location

# Étape 2 : Informations sur la voiture
class CarModelForm(forms.ModelForm):
    BRAND_CHOICES = [
        ("Abarth", "Abarth"),
        ("Alía-Romeo", "Alía-Romeo"),
        ("Alpine", "Alpine"),
        ("Audi", "Audi"),
        ("BMW", "BMW"),
        ("Bollore", "Bollore"),
        ("Chevrolet", "Chevrolet"),
        ("Chrysler", "Chrysler"),
        ("Citroen", "Citroën"),
        ("Cupra", "Cupra"),
        ("DS", "DS"),
        ("Dacia", "Dacia"),
        ("Daihatsu", "Daihatsu"),
        ("Fiat", "Fiat"),
        ("Ford", "Ford"),
        ("Honda", "Honda"),
        ("Hyundai", "Hyundai"),
        ("Infiniti", "Infiniti"),
        ("Innocenti", "Innocenti"),
        ("Isuzu", "Isuzu"),
        ("Iveco", "Iveco"),
        ("Jaguar", "Jaguar"),
        ("Jeep", "Jeep"),
        ("Lancia", "Lancia"),
        ("Land Rover", "Land Rover"),
        ("Lexus", "Lexus"),
        ("Lynk & Co", "Lynk & Co"),
        ("MG", "MG"),
        ("Man", "Man"),
        ("Maserati", "Maserati"),
        ("Maxus", "Maxus"),
        ("Mazda", "Mazda"),
        ("Mercedes-Benz", "Mercedes-Benz"),
        ("Mini", "Mini"),
        ("Mitsubishi", "Mitsubishi"),
        ("Mpm Motors", "Mpm Motors"),
        ("Nissan", "Nissan"),
        ("Opel", "Opel"),
        ("Peugeot", "Peugeot"),
        ("Plaggio", "Plaggio"),
        ("Porsche", "Porsche"),
        ("Renault", "Renault"),
        ("Rover", "Rover"),
        ("Saab", "Saab"),
        ("Seat", "Seat"),
        ("Skoda", "Skoda"),
        ("Smart", "Smart"),
        ("SsangYong", "SsangYong"),
        ("Subaru", "Subaru"),
        ("Suzuki", "Suzuki"),
        ("Tesla", "Tesla"),
        ("Toyota", "Toyota"),
        ("Triumph", "Triumph"),
        ("Tvr", "Tvr"),
        ("Volkswagen", "Volkswagen"),
        ("Volvo", "Volvo"),
    ]

    brand = forms.ChoiceField(
        choices=[("", "Sélectionnez une marque")] + BRAND_CHOICES,
        label="Marque de la voiture",
        widget=forms.Select(attrs={
            "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200 bg-white",
        }),
        error_messages={"required": "Ce champ est obligatoire."},
    )
    model = forms.CharField(
        label="Modèle de la voiture",
        widget=forms.TextInput(attrs={
            "placeholder": "Saisissez le modèle de la voiture",
            "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200 transition-shadow",
        }),
        error_messages={"required": "Ce champ est obligatoire."},
    )

    year = forms.IntegerField(
        label="Année de fabrication",
        widget=forms.NumberInput(attrs={
            "placeholder": "Saisissez l'année de fabrication de la voiture",
            "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200 transition-shadow",
        }),
        error_messages={"required": "Ce champ est obligatoire."},
        min_value=1955,
        max_value=datetime.now().year,
    )

    class Meta:
        model = Car
        fields = ["brand", "model", "year"]

# Étape 3 : Informations sur la voiture
class CarModelDetailsForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['transmission', 'fuel_type', 'seats']
        labels = {
            'transmission': "Transmission",
            'fuel_type': "Type de carburant",
            'seats': "Nombre de sièges",
        }
        widgets = {
            'transmission': forms.Select(attrs={
                "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200 bg-white"
            }),
            'fuel_type': forms.Select(attrs={
                "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200 bg-white"
            }),
            'seats': forms.Select(attrs={
                "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200",

            }),
        }

# Étape 4 : Anonnce
DUREE_CHOICES_MIN = [
    (1, "1 jour (recommandé)"),
    (2, "2 jours"),
    (3, "3 jours"),
]
DUREE_CHOICES_MAX = [
    (5, "5 jours"),
    (7, "1 semaine"),
    (14, "2 semaines"),
    (21, "3 semaines (recommandé)"),
    (30, "1 mois"),
]
class DispoForm(forms.ModelForm):
    duree_minimale = forms.TypedChoiceField(
        choices=DUREE_CHOICES_MIN,
        coerce=int,
        label="Durée minimale",
        widget=forms.Select(attrs={
            "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200 bg-white"
        }),
        error_messages={"required": "Veuillez choisir une durée minimale."},
    )

    duree_maximale = forms.TypedChoiceField(
        choices=DUREE_CHOICES_MAX,
        coerce=int,
        label="Durée maximale",
        widget=forms.Select(attrs={
            "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200 bg-white"
        }),
        error_messages={"required": "Veuillez choisir une durée maximale."},
    )

    class Meta:
        model = Annonce
        fields = ['duree_minimale', 'duree_maximale']

# Étape 5 : Informations sur l'annonce
class DescriptionForm(forms.ModelForm):
    
    price_per_day = forms.DecimalField(
        label="Prix par jour (DZD)",
        widget=forms.NumberInput(attrs={
            "class": "w-full h-12 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200",
            "placeholder":"Entrez un montant entre 2500 et 25000",
            "min": 2500,
            "max" : 25000,
        }),
        error_messages={"required": "Ce champ est obligatoire."},
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': "Vous n'avez pas besoin d'indiquer vos coordonnées ni les instructions de prise en charge. Elles seront transmises aux invités une fois leur réservation finalisée.",
            'class': 'w-full p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200 transition-shadow resize-none',
            'oninput': 'updateWordCount(this)',
        }),
        label="Description du véhicule",
        min_length=50,
        max_length=1000,
        required=True
    )
    
    class Meta:
        model = Annonce
        fields = ['price_per_day', 'description']
        labels = {
            'price_per_day': "Prix par jour (DZD)",
            'description': "Description",
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        print('>>>', data, initial)
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class CarImageForm(forms.ModelForm):
    image = MultipleFileField(required=False)
    class Meta:
        model = CarImage
        fields = ['image']