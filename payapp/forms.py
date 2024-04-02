from django import forms
from .models import Transaction


class TransactionForm(forms.Form):
    email = forms.EmailField(required=True, label='Email')
    reference = forms.CharField(required=True, max_length=50)
    amount = forms.IntegerField(required=True)

