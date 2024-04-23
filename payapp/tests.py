from django.contrib.sites import requests
from django.test import TestCase
from .forms import DirectPaymentForm, PaymentRequestForm
from register.models import User
from payapp.models import ExchangeRates
from payapp.converter import get_conversion_rate, CURRENCY_CONVERSION_URL
import requests


class TestDirectPaymentForm(TestCase):
    def setUp(self):
        user1 = User(username='test_user_1',
                     first_name='test_user',
                     last_name='1',
                     email='test_user_1@email.com',
                     phone_number='07123456789',
                     currency='£',
                     password='Password123!'
                     )
        user1.create_user()
        user2 = User(username='test_user_2',
                     first_name='test_user',
                     last_name='2',
                     email='test_user_2@email.com',
                     phone_number='07987654321',
                     currency='£',
                     password='Password123!'
                     )
        user2.create_user()

    def test_email_blank_validation(self):
        form = DirectPaymentForm(data={'receiver_email': ''})
        self.assertEqual(form.errors['receiver_email'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_email_exists_validation(self):
        form = DirectPaymentForm(data={'receiver_email': 'test_user_3@email.com'})
        self.assertEqual(form.errors['__all__'], ['No user exists with that email'])
        self.assertFalse(form.is_valid())

    def test_emails_same_validation(self):
        form = DirectPaymentForm(
            data={'receiver_email': 'test_user_1@email.com', 'sender_email': 'test_user_1@email.com'})
        self.assertEqual(form.errors['__all__'], ['You cannot send money to yourself'])
        self.assertFalse(form.is_valid())

    def test_reference_blank_validation(self):
        form = DirectPaymentForm(data={'reference': ''})
        self.assertEqual(form.errors['receiver_email'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_amount_blank_validation(self):
        form = DirectPaymentForm(data={'amount': None})
        self.assertEqual(form.errors['amount'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_user_has_amount_validation(self):
        form = DirectPaymentForm(
            data={'receiver_email': 'test_user_1@email.com', 'sender_email': 'test_user_2@email.com', 'amount': 10000})
        self.assertEqual(form.errors['__all__'], ['You do not contain the required funds to make this payment'])
        self.assertFalse(form.is_valid())


class TestPaymentRequestForm(TestCase):
    def setUp(self):
        user1 = User(username='test_user_1',
                     first_name='test_user',
                     last_name='1',
                     email='test_user_1@email.com',
                     phone_number='07123456789',
                     currency='£',
                     password='Password123!'
                     )
        user1.create_user()
        user2 = User(username='test_user_2',
                     first_name='test_user',
                     last_name='2',
                     email='test_user_2@email.com',
                     phone_number='07987654321',
                     currency='£',
                     password='Password123!'
                     )
        user2.create_user()

    def test_email_blank_validation(self):
        form = PaymentRequestForm(data={'receiver_email': ''})
        self.assertEqual(form.errors['receiver_email'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_email_exists_validation(self):
        form = PaymentRequestForm(data={'receiver_email': 'test_user_3@email.com'})
        print(form.errors)
        self.assertEqual(form.errors['__all__'], ['No user exists with that email'])
        self.assertFalse(form.is_valid())

    def test_emails_same_validation(self):
        form = PaymentRequestForm(
            data={'receiver_email': 'test_user_1@email.com', 'sender_email': 'test_user_1@email.com'})
        self.assertEqual(form.errors['__all__'], ['You cannot request money from yourself'])
        self.assertFalse(form.is_valid())

    def test_reference_blank_validation(self):
        form = PaymentRequestForm(data={'reference': ''})
        self.assertEqual(form.errors['receiver_email'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_amount_blank_validation(self):
        form = PaymentRequestForm(data={'amount': None})
        self.assertEqual(form.errors['amount'], ['This field is required.'])
        self.assertFalse(form.is_valid())


class TestCurrencyConverter(TestCase):
    def setUp(self):
        GBP_to_USD = ExchangeRates(from_currency='GBP', to_currency='USD', conversion_rate=1.23)
        USD_to_GBP = ExchangeRates(from_currency='USD', to_currency='GBP', conversion_rate=0.81)
        GBP_to_EUR = ExchangeRates(from_currency='GBP', to_currency='EUR', conversion_rate=1.16)
        EUR_to_GBP = ExchangeRates(from_currency='EUR', to_currency='GBP', conversion_rate=0.86)
        EUR_to_USD = ExchangeRates(from_currency='EUR', to_currency='USD', conversion_rate=1.06)
        USD_to_EUR = ExchangeRates(from_currency='USD', to_currency='EUR', conversion_rate=0.94)
        GBP_to_USD.save()
        USD_to_GBP.save()
        GBP_to_EUR.save()
        EUR_to_GBP.save()
        EUR_to_USD.save()
        USD_to_EUR.save()

    def test_GBP_to_USD_conversion(self):
        balance = 1000
        conversion_rate = get_conversion_rate(from_currency='GBP', to_currency='USD')
        balance = balance * conversion_rate
        self.assertEqual(balance, 1000 * 1.23)

    def test_USD_to_GBP_conversion(self):
        balance = 1000
        conversion_rate = get_conversion_rate(from_currency='USD', to_currency='GBP')
        balance = balance * conversion_rate
        self.assertEqual(balance, 1000 * 0.81)

    def test_GBP_to_EUR_conversion(self):
        balance = 1000
        conversion_rate = get_conversion_rate(from_currency='GBP', to_currency='EUR')
        balance = balance * conversion_rate
        self.assertEqual(balance, 1000 * 1.16)

    def test_EUR_to_GBP_conversion(self):
        balance = 1000
        conversion_rate = get_conversion_rate(from_currency='EUR', to_currency='GBP')
        balance = balance * conversion_rate
        self.assertEqual(balance, 1000 * 0.86)

    def test_EUR_to_USD_conversion(self):
        balance = 1000
        conversion_rate = get_conversion_rate(from_currency='EUR', to_currency='USD')
        balance = balance * conversion_rate
        self.assertEqual(balance, 1000 * 1.06)

    def test_USD_to_EUR_conversion(self):
        balance = 1000
        conversion_rate = get_conversion_rate(from_currency='USD', to_currency='EUR')
        balance = balance * conversion_rate
        self.assertEqual(balance, 1000 * 0.94)

    def test_invalid_currency(self):
        response = requests.get(CURRENCY_CONVERSION_URL + 'AUD/GBP/')
        result = response.json()
        self.assertEqual(result, {'detail': 'No ExchangeRates matches the given query.'})

