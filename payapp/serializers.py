from django.contrib.auth.models import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, generics
from payapp.models import ExchangeRates
from webapps2024.settings import CURRENCY_CONVERSION_URL
import requests


class Currencies(models.TextChoices):
    GBP = 'GBP', _('GBP')
    EUR = 'EUR', _('EUR')
    USD = 'USD', _('USD')


def is_valid_currency(currency):
    return currency == Currencies.GBP or currency == Currencies.USD or currency == Currencies.EUR


class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRates
        fields = '__all__'


class Conversion(generics.RetrieveAPIView):
    serializer_class = ConversionSerializer

    def get_object(self):
        from_currency = self.kwargs.get('from_currency')
        to_currency = self.kwargs.get('to_currency')
        if is_valid_currency(from_currency) and is_valid_currency(from_currency):
            return ExchangeRates.objects.get(from_currency=from_currency, to_currency=to_currency)


def get_conversion_rate(from_currency, to_currency):
    response = requests.get(CURRENCY_CONVERSION_URL + from_currency + '/' + to_currency + '/')
    exchange_rate = response.json()
    return exchange_rate['conversion_rate']


def convert_funds(amount, conversion_rate):
    return amount * conversion_rate
