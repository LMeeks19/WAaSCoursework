from .server import get_user_by_email
from .models import Transaction, TransactionStatus, TransactionType
from datetime import datetime


def create_direct_payment(sender_email, receiver_email, reference, amount):
    transaction = Transaction(
        sender_email=sender_email,
        receiver_email=receiver_email,
        reference=reference,
        amount=amount,
        send_date=datetime.utcnow(),
        status=TransactionStatus.CLEARED,
        type=TransactionType.DIRECT
    )
    update_user_balances(user_to_decrease_email=transaction.sender_email, user_to_increase_email=transaction.receiver_email, transaction_amount=transaction.amount)
    transaction.save()


def update_user_balances(user_to_decrease_email, user_to_increase_email, transaction_amount):
    user_to_decrease = get_user_by_email(user_to_decrease_email)
    user_to_increase = get_user_by_email(user_to_increase_email)
    user_to_decrease.balance = user_to_decrease.balance - transaction_amount
    user_to_increase.balance = user_to_increase.balance + transaction_amount
    user_to_increase.save()
    user_to_decrease.save()


def create_payment_request(sender_email, receiver_email, reference, amount):
    transaction = Transaction(
        sender_email=sender_email,
        receiver_email=receiver_email,
        reference=reference,
        amount=amount,
        send_date=datetime.utcnow(),
        status=TransactionStatus.PENDING,
        type=TransactionType.REQUEST
    )
    transaction.save()


def accept_payment_request(transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    transaction.status = TransactionStatus.CLEARED
    update_user_balances(user_to_decrease_email=transaction.receiver_email, user_to_increase_email=transaction.sender_email, transaction_amount=transaction.amount)
    transaction.save()


def reject_payment_request(transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    transaction.status = TransactionStatus.REJECTED
    transaction.save()
