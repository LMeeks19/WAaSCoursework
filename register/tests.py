from django.test import TestCase
from .forms import RegisterForm
from .models import User
from payapp.converter import Currencies, is_valid_currency


class TestRegisterForm(TestCase):
    def setUp(self):
        user = User(username='test_user_1',
                    first_name='test_user',
                    last_name='1',
                    email='test_user_1@email.com',
                    phone_number='07123456789',
                    currency=Currencies.GBP,
                    password='Password123!'
                    )
        user.create_user()

    def test_username_blank_validation(self):
        form = RegisterForm(data={'username': '', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_username_exists_validation(self):
        form = RegisterForm(data={'username': 'test_user_1', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['username'], ['Username already in use'])
        self.assertFalse(form.is_valid())

    def test_first_name_blank_validation(self):
        form = RegisterForm(data={'first_name': '', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_last_name_exists_validation(self):
        form = RegisterForm(data={'last_name': '', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['last_name'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_email_blank_validation(self):
        form = RegisterForm(data={'email': '', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['email'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_email_exists_validation(self):
        form = RegisterForm(data={'email': 'test_user_1@email.com', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['email'], ['Email already in use'])
        self.assertFalse(form.is_valid())

    def test_phone_number_blank_validation(self):
        form = RegisterForm(data={'phone_number': '', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['phone_number'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_phone_number_exists_validation(self):
        form = RegisterForm(data={'phone_number': '07123456789', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['phone_number'], ['Phone Number already in use'])
        self.assertFalse(form.is_valid())

    def test_currency_blank_validation(self):
        form = RegisterForm(data={'currency': ''})
        self.assertEqual(form.errors['currency'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_is_valid_currency_validation(self):
        form = RegisterForm(data={'currency': Currencies.GBP})
        currency = form.data.get('currency')
        self.assertTrue(is_valid_currency(currency))
        self.assertFalse(form.is_valid())

    def test_is_invalid_currency_validation(self):
        form = RegisterForm(data={'currency': 'AUD'})
        currency = form.data.get('currency')
        self.assertFalse(is_valid_currency(currency))
        self.assertFalse(form.is_valid())

    def test_password_1_blank_validation(self):
        form = RegisterForm(data={'password1': '', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['password1'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_password_1_length_validation(self):
        form = RegisterForm(data={'password1': 'Pa1!', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 8 characters'])
        self.assertFalse(form.is_valid())

    def test_password_1_uppercase_validation(self):
        form = RegisterForm(data={'password1': 'password123!', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 1 uppercase character'])
        self.assertFalse(form.is_valid())

    def test_password_1_lowercase_validation(self):
        form = RegisterForm(data={'password1': 'PASSWORD123!', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 1 lowercase character'])
        self.assertFalse(form.is_valid())

    def test_password_1_digit_validation(self):
        form = RegisterForm(data={'password1': 'Password!', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 1 number character'])
        self.assertFalse(form.is_valid())

    def test_password_1_special_validation(self):
        form = RegisterForm(data={'password1': 'Password123', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 1 special character'])
        self.assertFalse(form.is_valid())

    def test_password_1_space_validation(self):
        form = RegisterForm(data={'password1': 'Password 123!', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['password1'], ['Password must not contain any whitespace characters'])
        self.assertFalse(form.is_valid())

    def test_password_2_blank_validation(self):
        form = RegisterForm(data={'password2': '', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['password2'], ['This field is required.'])
        self.assertFalse(form.is_valid())

    def test_password_2_match_validation(self):
        form = RegisterForm(data={'password1': 'Password123!', 'password2': 'Password456!', 'currency': Currencies.GBP})
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])
        self.assertFalse(form.is_valid())
