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
