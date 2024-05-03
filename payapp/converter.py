from django.contrib.auth.models import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, generics
from payapp.models import ExchangeRates
import requests


# The 'localhost' aspect of this URL will be changed to what ever the current EC2 instance public IP address
# is when asked to run the server for the additional marks
CURRENCY_CONVERSION_URL = 'http://localhost:8000/webapps2024/conversion/'


# Enum of currency types
class Currencies(models.TextChoices):
    GBP = 'GBP', _('GBP')
    EUR = 'EUR', _('EUR')
    USD = 'USD', _('USD')


# Checks to see if the inputted currency is a valid currency
def is_valid_currency(currency):
    return currency == Currencies.GBP or currency == Currencies.USD or currency == Currencies.EUR


# Rest framework serializer
class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRates
        fields = '__all__'


class Conversion(generics.RetrieveAPIView):
    serializer_class = ConversionSerializer
    queryset = ExchangeRates.objects.all()

    def get_object(self):
        from_currency = self.kwargs.get('from_currency')
        to_currency = self.kwargs.get('to_currency')
        exchange_rate = get_object_or_404(self.get_queryset(), from_currency=from_currency, to_currency=to_currency)
        return exchange_rate


# Method to retrieve the currency conversion
def get_conversion_rate(from_currency, to_currency):
    response = requests.get(CURRENCY_CONVERSION_URL + from_currency + '/' + to_currency + '/')
    result = response.json()
    if not response.status_code == 200:
        return result['detail']
    return result['conversion_rate']


# formula for currency conversion
def convert_funds(amount, conversion_rate):
    return amount * conversion_rate
