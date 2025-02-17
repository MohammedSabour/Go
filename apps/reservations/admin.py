from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "car",
        "renter",
        "start_date",
        "end_date",
        "status", 
        "total_price",
        "created_at",
    )
    list_filter = ("status", "created_at", "start_date")
    search_fields = ['car','renter__username']
    ordering = ("-created_at",)

    readonly_fields = (
        "car",
        "renter",
        "total_price",
        "created_at",
        "updated_at",
        "status",
    )  # Tous les champs sont en lecture seule pour empêcher toute modification
