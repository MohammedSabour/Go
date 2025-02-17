from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Car(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING, 'En attente de vérification'),
        (APPROVED, 'Approuvée'),
        (REJECTED, 'Rejetée'),
    ]

    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars', verbose_name="Propriétaire")
    brand = models.CharField(max_length=100, verbose_name="Marque")
    model = models.CharField(max_length=100, verbose_name="Modèle")
    year = models.PositiveIntegerField(verbose_name="Année de fabrication")
    fuel_type = models.CharField(
        max_length=50,
        choices=[
            ('gasoline', 'Essence'),
            ('diesel', 'Diesel'),
            ('electric', 'Électrique'),
            ('hybrid', 'Hybride'),
        ],
        verbose_name="Type de carburant"
    )
    transmission = models.CharField(
        max_length=50,
        choices=[
            ('manual', 'Manuelle'),
            ('automatic', 'Automatique'),
        ],
        verbose_name="Transmission"
    )
    seats = models.PositiveIntegerField(
        choices=[
            (2, "2 sièges"),
            (4, "4 sièges"),
            (5, "5 sièges"),
            (7, "7 sièges"),
            (9, "9 sièges"),
        ],
        verbose_name="Nombre de sièges"
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name="Statut"
    )
    rejection_reason = models.TextField(blank=True, null=True, verbose_name="Raison du rejet")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def clean(self):
        """Validation personnalisée pour éviter les combinaisons incohérentes."""
        if self.transmission == "manual" and self.fuel_type == "electric":
            raise ValidationError(
                {"fuel_type": "Les voitures électriques n'ont pas de transmission manuelle."}
            )
        if self.status == self.APPROVED:
            self.rejection_reason = None  # Réinitialise la raison du rejet si la voiture est approuvée
        elif self.status == self.REJECTED and not self.rejection_reason:
            self.rejection_reason = "Veuillez vérifier les informations"
    
        super().clean()
    
    # Functions
    def approve(self):
        """Approuve la voiture pour la location."""
        self.status = self.APPROVED
        self.rejection_reason = None
        self.save()

    def reject(self, reason=None):
        """Rejette la voiture et enregistre la raison, avec une valeur par défaut si aucune raison n'est fournie."""
        self.status = self.REJECTED
        self.rejection_reason = reason if reason else "Raison non spécifiée"
        self.full_clean()
        self.save()

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.owner.username}"
    

    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"
        ordering = ['-created_at']


class Annonce(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name="annonce")
    description = models.TextField(verbose_name="Description")
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix par jour (DZD)")
    
    # Disponibilité
    duree_minimale = models.PositiveIntegerField(default=1, help_text="Durée minimale de location en jours")
    duree_maximale = models.PositiveIntegerField(default=21, help_text="Durée maximale de location en jours")

    # Activation de l'annonce
    is_active = models.BooleanField(default=True, verbose_name="Annonce active ?")

    def __str__(self):
        return f"Annonce de {self.car.brand} {self.car.model}"

    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"


class CarImage(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name="images", verbose_name="Annonce associée")
    image = models.ImageField(upload_to='cars/images/', verbose_name="Image")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de téléversement")

    def __str__(self):
        return f"Image pour {self.annonce.car.brand} {self.annonce.car.model} ({self.uploaded_at})"
