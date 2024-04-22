from register.models import User
from payapp.models import Transaction, TransactionStatus, TransactionType
from django.db.models import Q
import requests


def get_conversion_rate(from_currency, to_currency):
    response = requests.get('http://localhost:10000/webapps2024/conversion/' + from_currency + '/' + to_currency + '/')
    exchange_rate = response.json()
    return exchange_rate['conversion_rate']


def get_all_transactions():
    return list(Transaction.objects.all())


def get_all_users():
    return list(User.objects.all().order_by('-is_superuser'))


def get_user_by_email(user_email):
    return User.objects.get(email=user_email)


def get_all_user_transactions(user_email):
    return list(Transaction.objects.filter(Q(sender_email=user_email) | Q(receiver_email=user_email)).order_by('-send_date'))


def get_user_cleared_transactions(user_email):
    return list(Transaction.objects.filter(status=TransactionStatus.CLEARED).filter(Q(sender_email=user_email) | Q(receiver_email=user_email)).order_by('-send_date'))


def get_user_sent_direct_payments(user_email):
    return list(Transaction.objects.filter(sender_email=user_email, type=TransactionType.DIRECT).order_by('-send_date'))


def get_user_sent_payment_requests(user_email):
    return list(Transaction.objects.filter(type=TransactionType.REQUEST, sender_email=user_email).order_by('-send_date'))


def get_user_received_payment_requests(user_email):
    return list(Transaction.objects.filter(type=TransactionType.REQUEST, receiver_email=user_email).order_by('-send_date'))


def get_user(user_id):
    return User.objects.get(id=user_id)


def get_user_by_username(username):
    return User.objects.get(username=username)


def get_transaction(transaction_id):
    return Transaction.objects.get(id=transaction_id)





