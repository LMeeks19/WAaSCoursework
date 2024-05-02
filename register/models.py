from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import models


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True)
    balance = models.FloatField()
    currency = models.CharField(max_length=8)

    def create_user(self):
        user = User(username=self.username,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    email=self.email,
                    phone_number=self.phone_number,
                    currency=self.currency,
                    password=self.password,
                    balance=1000,
                    is_superuser=False,
                    is_staff=False)
        user.set_password(user.password)
        user.save()

    def create_admin(self):
        user = User(username=self.username,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    email=self.email,
                    phone_number=self.phone_number,
                    currency=self.currency,
                    password=self.password,
                    balance=1000,
                    is_superuser=True,
                    is_staff=True)
        user.set_password(user.password)
        user.save()

    def get_currency_symbol(self):
        if self.currency == "GBP":
            return "£"
        if self.currency == "EUR":
            return "€"
        if self.currency == "USD":
            return "$"

