from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Adresse email", widget=forms.EmailInput(attrs={'class': 'input'}))