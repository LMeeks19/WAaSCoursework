from django.contrib.auth.models import models
from django.utils.translation import gettext_lazy as _


class Currencies(models.TextChoices):
    GBP = 'GBP', _('GBP')
    EUR = 'EUR', _('EUR')
    USD = 'USD', _('USD')
