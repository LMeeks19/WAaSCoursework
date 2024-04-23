from .server import get_user_by_email
from .models import Transaction, TransactionStatus, TransactionType
from .converter import get_conversion_rate, convert_funds


def create_direct_payment(sender_email, receiver_email, reference, amount):
    sender = get_user_by_email(sender_email)
    receiver = get_user_by_email(receiver_email)

    sender_amount = amount
    receiver_amount = amount
    if not sender.currency == receiver.currency:
        result = get_conversion_rate(sender.currency, receiver.currency)
        if not isinstance(result, float):
            return result
        receiver_amount = convert_funds(amount, result)

    transaction = Transaction(
        sender_email=sender.email,
        sender_currency=sender.currency,
        sender_amount=round(sender_amount, 2),
        receiver_email=receiver.email,
        receiver_currency=receiver.currency,
        receiver_amount=round(receiver_amount, 2),
        reference=reference,
        status=TransactionStatus.CLEARED,
        type=TransactionType.DIRECT
    )
    update_user_balances_direct(transaction)
    transaction.save()
    return transaction


def create_payment_request(sender_email, receiver_email, reference, amount):
    sender = get_user_by_email(sender_email)
    receiver = get_user_by_email(receiver_email)

    sender_amount = amount
    receiver_amount = amount
    if not sender.currency == receiver.currency:
        result = get_conversion_rate(sender.currency, receiver.currency)
        if not isinstance(result, float):
            return result
        receiver_amount = convert_funds(amount, result)

    transaction = Transaction(
        sender_email=sender.email,
        sender_currency=sender.currency,
        sender_amount=round(sender_amount, 2),
        receiver_email=receiver.email,
        receiver_currency=receiver.currency,
        receiver_amount=round(receiver_amount, 2),
        reference=reference,
        status=TransactionStatus.PENDING,
        type=TransactionType.REQUEST
    )
    transaction.save()
    return transaction


def update_user_balances_direct(transaction):
    sender = get_user_by_email(transaction.sender_email)
    receiver = get_user_by_email(transaction.receiver_email)

    sender.balance = sender.balance - transaction.sender_amount
    receiver.balance = receiver.balance + transaction.receiver_amount

    sender.save()
    receiver.save()


def update_user_balances_request(transaction):
    sender = get_user_by_email(transaction.sender_email)
    receiver = get_user_by_email(transaction.receiver_email)

    sender.balance = sender.balance + transaction.sender_amount
    receiver.balance = receiver.balance - transaction.receiver_amount

    sender.save()
    receiver.save()


def accept_payment_request(transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    update_user_balances_request(transaction)
    transaction.status = TransactionStatus.CLEARED
    transaction.save()


def reject_payment_request(transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    transaction.status = TransactionStatus.REJECTED
    transaction.save()
