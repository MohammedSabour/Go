from django.contrib import admin
from .models import Car, Annonce, CarImage

class AnnonceInline(admin.StackedInline):  
    model = Annonce
    extra = 0

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    verbose_name = "Image supplémentaire"
    verbose_name_plural = "Images supplémentaires"

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "owner", "status")
    list_filter = ("status", "fuel_type", "transmission")
    search_fields = ("brand", "model", "owner__username")
    actions = ["approve_car", "reject_car"]
    inlines = [AnnonceInline]

    def approve_car(self, request, queryset):
        for car in queryset:
            car.approve()
        self.message_user(request, "Les voitures sélectionnées ont été approuvées.")


    def reject_car(self, request, queryset):
        for car in queryset:
            car.reject("Veuillez vérifier les informations")
        self.message_user(request, "Les voitures sélectionnées ont été refusées.")


    approve_car.short_description = "✅ Approuver les voitures sélectionnées"
    reject_car.short_description = "❌ Refuser les voitures sélectionnées"

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ("car", "price_per_day")
    list_filter = ("price_per_day",)
    search_fields = ("voiture__brand", "voiture__model")
    inlines = [CarImageInline]

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ("annonce", "uploaded_at")
