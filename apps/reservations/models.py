from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from apps.listings.models import Car

class Reservation(models.Model):
    # Statut de la réservation
    REQUESTED = 'requested'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    PAID = 'paid'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (REQUESTED, 'Demandée'),
        (ACCEPTED, 'Acceptée'),
        (DECLINED, 'Refusée'),
        (PAID, 'Payée'),
        (ONGOING, 'En cours'),
        (COMPLETED, 'Terminée'),
        (CANCELED, 'Annulée'),
    ]

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    renter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="car_reservations"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default=REQUESTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        """Calcule automatiquement le prix total."""
        days = (self.end_date - self.start_date).days + 1
        self.total_price = days * self.car.price_per_day

    def save(self, *args, **kwargs):
        """Override de la méthode save pour calculer le prix automatiquement."""
        if not self.total_price:
            self.calculate_total_price()
        super().save(*args, **kwargs)

    def accept_reservation(self):
        """Accepter la réservation."""
        self.status = self.ACCEPTED
        self.save()

    def decline_reservation(self):
        """Refuser la réservation."""
        self.status = self.DECLINED
        self.save()

    def mark_paid(self):
        """Marquer la réservation comme payée."""
        self.status = self.PAID
        self.save()

    def start_reservation(self):
        """Commencer la réservation."""
        self.status = self.ONGOING
        self.save()

    def complete_reservation(self):
        """Terminer la réservation."""
        self.status = self.COMPLETED
        self.save()

    def cancel_reservation(self):
        """Annuler la réservation."""
        self.status = self.CANCELED
        self.save()

    def __str__(self):
        return f"Reservation for {self.car} by {self.renter.username} - {self.status}"
