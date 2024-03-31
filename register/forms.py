from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from phonenumber_field.modelfields import PhoneNumberField


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Forename")
    last_name = forms.CharField(required=True, label="Surname")
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone_number")
