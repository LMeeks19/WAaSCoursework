from django.test import TestCase
from .forms import RegisterForm
from register.models import User
from payapp.converter import Currencies


class TestRegisterForm(TestCase):
    def setUp(self):
        user = User(username='test_user_1',
                    first_name='test_user',
                    last_name='1',
                    email='test_user_1@email.com',
                    phone_number='07123456789',
                    currency='£',
                    password='Password123!'
                    )
        user.create_user()

    def test_username_blank_validation(self):
        form = RegisterForm(data={'username': ''})
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_username_exists_validation(self):
        form = RegisterForm(data={'username': 'test_user_1'})
        self.assertEqual(form.errors['username'], ['Username already in use'])

    def test_first_name_blank_validation(self):
        form = RegisterForm(data={'first_name': ''})
        self.assertEqual(form.errors['first_name'], ['This field is required.'])

    def test_last_name_exists_validation(self):
        form = RegisterForm(data={'last_name': ''})
        self.assertEqual(form.errors['last_name'], ['This field is required.'])

    def test_email_blank_validation(self):
        form = RegisterForm(data={'email': ''})
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def test_email_exists_validation(self):
        form = RegisterForm(data={'email': 'test_user_1@email.com'})
        self.assertEqual(form.errors['email'], ['Email already in use'])

    def test_phone_number_blank_validation(self):
        form = RegisterForm(data={'phone_number': ''})
        self.assertEqual(form.errors['phone_number'], ['This field is required.'])

    def test_phone_number_exists_validation(self):
        form = RegisterForm(data={'phone_number': '07123456789'})
        self.assertEqual(form.errors['phone_number'], ['Phone Number already in use'])

    def test_currency_blank_validation(self):
        form = RegisterForm(data={'currency': ''})
        self.assertEqual(form.errors['currency'], ['This field is required.'])

    def test_is_valid_currency_validation(self):
        form = RegisterForm(data={'currency': 'GBP'})
        currency = form.data.get('currency')
        self.assertTrue((Currencies.EUR == currency) or (Currencies.GBP == currency) or (Currencies.USD == currency))

    def test_is_invalid_currency_validation(self):
        form = RegisterForm(data={'currency': 'AUD'})
        currency = form.data.get('currency')
        self.assertFalse((Currencies.EUR == currency) or (Currencies.GBP == currency) or (Currencies.USD == currency))

    def test_password_1_blank_validation(self):
        form = RegisterForm(data={'password1': ''})
        self.assertEqual(form.errors['password1'], ['This field is required.'])

    def test_password_1_length_validation(self):
        form = RegisterForm(data={'password1': 'Pa1!'})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 8 characters'])

    def test_password_1_uppercase_validation(self):
        form = RegisterForm(data={'password1': 'password123!'})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 1 uppercase character'])

    def test_password_1_lowercase_validation(self):
        form = RegisterForm(data={'password1': 'PASSWORD123!'})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 1 lowercase character'])

    def test_password_1_digit_validation(self):
        form = RegisterForm(data={'password1': 'Password!'})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 1 number character'])

    def test_password_1_special_validation(self):
        form = RegisterForm(data={'password1': 'Password123'})
        self.assertEqual(form.errors['password1'], ['Password must contain at least 1 special character'])

    def test_password_1_space_validation(self):
        form = RegisterForm(data={'password1': 'Password 123!'})
        self.assertEqual(form.errors['password1'], ['Password must not contain any whitespace characters'])

    def test_password_2_blank_validation(self):
        form = RegisterForm(data={'password2': ''})
        self.assertEqual(form.errors['password2'], ['This field is required.'])

    def test_password_2_match_validation(self):
        form = RegisterForm(data={'password1': 'Password123!', 'password2': 'Password456!'})
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])


