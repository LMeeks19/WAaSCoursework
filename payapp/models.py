import django.utils.timezone
from django.db import models


# Transaction status enum
class TransactionStatus(models.TextChoices):
    PENDING = 'PENDING',
    CLEARED = 'CLEARED',
    REJECTED = 'REJECTED',


# Transaction type enum
class TransactionType(models.TextChoices):
    DIRECT = 'DIRECT',
    REQUEST = 'REQUEST',


# Transaction model
class Transaction(models.Model):
    sender_email = models.EmailField()
    sender_currency = models.CharField(max_length=3)
    sender_amount = models.FloatField()
    receiver_email = models.EmailField()
    receiver_currency = models.CharField(max_length=3)
    receiver_amount = models.FloatField()
    reference = models.CharField(max_length=50)
    send_date = models.DateTimeField(default=django.utils.timezone.now)
    status = models.CharField(max_length=8)
    type = models.CharField(max_length=7)

    def get_sender_currency_symbol(self):
        if self.sender_currency == "GBP":
            return "£"
        if self.sender_currency == "EUR":
            return "€"
        if self.sender_currency == "USD":
            return "$"

    def get_receiver_currency_symbol(self):
        if self.receiver_currency == "GBP":
            return "£"
        if self.receiver_currency == "EUR":
            return "€"
        if self.receiver_currency == "USD":
            return "$"


# Exchange Rates model
class ExchangeRates(models.Model):
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    conversion_rate = models.FloatField()
