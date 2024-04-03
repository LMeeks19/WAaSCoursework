from register.models import User
from payapp.models import Transaction, TransactionStatus, TransactionType
from django.db.models import Q


def get_all_cleared_transaction():
    return list(Transaction.objects.filter(status=TransactionStatus.CLEARED))


def get_all_users():
    return list(User.objects.all().order_by('-is_superuser'))


def get_user_by_email(user_email):
    return User.objects.get(email=user_email)


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


def get_transaction(transaction_id):
    return Transaction.objects.get(id=transaction_id)





