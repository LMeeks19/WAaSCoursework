from django import forms
from register.models import User
from django.core.exceptions import ObjectDoesNotExist


class DirectPaymentForm(forms.Form):
    sender_email = forms.EmailField(required=True, label=False, widget=forms.HiddenInput())
    receiver_email = forms.EmailField(required=True, label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'email-field', 'autocomplete': 'off'}))
    reference = forms.CharField(required=True, max_length=50, label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Reference', 'class': 'reference-field', 'autocomplete': 'off'}))
    amount = forms.FloatField(required=True, label=False, widget=forms.NumberInput(
        attrs={'placeholder': 'Amount', 'class': 'amount-field', 'autocomplete': 'off'}))

    def clean_receiver_email(self):
        receiver_email = self.cleaned_data.get('receiver_email')
        sender_email = self.cleaned_data.get('sender_email')
        try:
            User.objects.get(email=receiver_email)
        except ObjectDoesNotExist:
            self.add_error(None, 'No user exists with that email')

        if receiver_email == sender_email:
            self.add_error(None, 'You cannot send money to yourself')
        return receiver_email

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        sender_email = self.cleaned_data.get('sender_email')
        if User.objects.get(email=sender_email).balance < amount:
            self.add_error(None, 'You do not contain the required funds to make this payment')
        return amount


class PaymentRequestForm(forms.Form):
    sender_email = forms.EmailField(required=True, label=False, widget=forms.HiddenInput())
    receiver_email = forms.EmailField(required=True, label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'email-field', 'autocomplete': 'off'}))
    reference = forms.CharField(required=True, max_length=50, label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Reference', 'class': 'reference-field', 'autocomplete': 'off'}))
    amount = forms.FloatField(required=True, label=False, widget=forms.NumberInput(
        attrs={'placeholder': 'Amount', 'class': 'amount-field', 'autocomplete': 'off'}))

    def clean_receiver_email(self):
        receiver_email = self.cleaned_data.get('receiver_email')
        sender_email = self.cleaned_data.get('sender_email')
        try:
            User.objects.get(email=receiver_email)
        except ObjectDoesNotExist:
            self.add_error(None, 'No user exists with that email')

        if receiver_email == sender_email:
            self.add_error(None, 'You cannot request money from yourself')
        return receiver_email
