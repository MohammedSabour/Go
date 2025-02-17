from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm
from apps.listings.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        terms = request.POST.get("terms")

        # Vérification des champs obligatoires
        if not all([first_name, last_name, email, password, terms]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, "register.html")

        # Vérifier si l'email existe déjà
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, "register.html")

        # Vérifier la longueur du mot de passe
        if len(password) < 6:
            messages.error(request, "Le mot de passe doit contenir au moins 6 caractères.")
            return render(request, "register.html")

        # Création de l'utilisateur
        user = User.objects.create_user(
            username=email, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        user.save()

        # Connexion automatique après inscription
        login(request, user)

        messages.success(request, "Inscription réussie ! Vous êtes maintenant connecté.")
        return redirect("home")

    return render(request, "register.html")


def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(data=request.POST)  
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_staff or user.is_superuser:
                    form.add_error(None, "Accès refusé : vous ne pouvez pas vous connecter ici en tant qu'administrateur.")
                    return render(request, "login.html", {"form": form})

                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Email ou mot de passe incorrect")

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

def dashboard_view(request):
    vehicule = Car.objects.filter(owner=request.user).first()
    return render(request, "hote/dashboard.html",{'vehicule': vehicule})

@csrf_exempt
def toggle_annonce(request, car_id):
    """Active/Désactive l'annonce d'une voiture."""
    if request.method == "POST":
        car = get_object_or_404(Car, id=car_id, owner=request.user)

        # Vérifie si une annonce existe pour la voiture
        annonce = getattr(car, 'annonce', None)
        if not annonce:
            return JsonResponse({"success": False, "error": "Aucune annonce trouvée."}, status=404)

        # Inverser l'état d'activation
        annonce.is_active = not annonce.is_active
        annonce.save()

        return JsonResponse({"success": True, "is_active": annonce.is_active})

    return JsonResponse({"success": False, "error": "Méthode non autorisée."}, status=405)

