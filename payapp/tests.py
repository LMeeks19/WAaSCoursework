from django.test import TestCase
from .forms import DirectPaymentForm, PaymentRequestForm
from register.models import User


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
        form = DirectPaymentForm(data={'receiver_email': 'test_user_1@email.com', 'sender_email': 'test_user_1@email.com'})
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
        form = DirectPaymentForm(data={'receiver_email': 'test_user_1@email.com', 'sender_email': 'test_user_2@email.com', 'amount': 10000})
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
        form = PaymentRequestForm(data={'receiver_email': 'test_user_1@email.com', 'sender_email': 'test_user_1@email.com'})
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
