from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Currencies
from phonenumber_field.modelfields import PhoneNumberField


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True, label="Forename")
    last_name = forms.CharField(required=True, label="Surname")
    email = forms.EmailField(required=True)
    phone_number = PhoneNumberField()
    currency = forms.ChoiceField(required=True, choices=Currencies.choices)
    password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'password'}))
    password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'password'}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone_number", "currency", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is None:
            self.add_error("username", "Username cannot be left blank")
        elif User.objects.filter(username=username).exists():
            self.add_error("username", "Username already in use")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            self.add_error("email", "Email cannot be left blank")
        elif User.objects.filter(email=email).exists():
            self.add_error("email", "Email already in use")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number is None:
            self.add_error("phone_number", "Phone Number cannot be left blank")
        elif User.objects.filter(phone_number=phone_number).exists():
            self.add_error("phone_number", "Phone Number already in use")
        return phone_number

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name is None:
            self.add_error("first_name", "Forename cannot be left blank")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name is None:
            self.add_error("last_name", "Surname cannot be left blank")
        return last_name

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            self.add_error("password1", "Password must contain at least 8 characters")
        if not any(char.isdigit() for char in password1):
            self.add_error("password1", "Password must contain at least 1 number character")
        if not any(char.isupper() for char in password1):
            self.add_error("password1", "Password must contain at least 1 uppercase character")
        if not any(char.islower() for char in password1):
            self.add_error("password1", "Password must contain at least 1 lowercase character")
        if not any(not char.isalnum() and not char.isspace() for char in password1):
            self.add_error("password1", "Password must contain at least 1 special character")
        if any(char.isspace() for char in password1):
            self.add_error("password1", "Password must not contain any whitespace characters")
        return password1
