from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from payapp.converter import get_conversion_rate, convert_funds, Currencies, is_valid_currency


# Registration form and all of its validation
class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'autocomplete': 'off'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Forename', 'autocomplete': 'off'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Surname', 'autocomplete': 'off'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off'}))
    phone_number = forms.CharField(required=True, label='Phone Number', widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Phone Number', 'autocomplete': 'off'}))
    currency = forms.ChoiceField(required=True, choices=Currencies.choices, widget=forms.Select(attrs={'autocomplete': 'off'}))
    password1 = forms.CharField(required=True, label='Password', widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Password', 'autocomplete': 'off'}))
    password2 = forms.CharField(required=True, label='Confirm Password', widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Confirm Password', 'autocomplete': 'off'}))
    balance = forms.FloatField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone_number", "currency", "password1", "password2", "balance")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error("username", "Username already in use")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error("email", "Email already in use")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            self.add_error("phone_number", "Phone Number already in use")
        return phone_number

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

    # Sets the balance for the user depending on the currency they choose
    def clean_balance(self):
        balance = 1000
        to_currency = Currencies.GBP
        if is_valid_currency(self.data['currency']):
            to_currency = self.cleaned_data['currency']
        if not to_currency == Currencies.GBP:
            conversion_rate = get_conversion_rate(from_currency=Currencies.GBP, to_currency=to_currency)
            balance = convert_funds(balance, conversion_rate)
        return balance
