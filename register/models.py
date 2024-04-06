from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import models
from django.utils.translation import gettext_lazy as _


class Currencies(models.TextChoices):
    GBP = '£', _('GBP £')
    EUR = '€', _('EUR €')
    USD = '$', _('USD $')


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True)
    balance = models.IntegerField(default=10000)
    currency = models.CharField(default='£', max_length=8)

    def create_user(self):
        user = User(username=self.username,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    email=self.email,
                    phone_number=self.phone_number,
                    currency=self.currency,
                    password=self.password,
                    is_superuser=False,
                    is_staff=False)
        user.save()

    def create_admin(self):
        user = User(username=self.username,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    email=self.email,
                    phone_number=self.phone_number,
                    currency=self.currency,
                    password=self.password,
                    is_superuser=True,
                    is_staff=True)
        user.save()

