from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Currencies
from django.contrib.auth.models import models


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Forename")
    last_name = forms.CharField(required=True, label="Surname")
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, label="Phone Number", widget=forms.TextInput(attrs={'type': 'tel'}))
    currency = forms.ChoiceField(required=True, choices=Currencies.choices)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone_number", "currency")
