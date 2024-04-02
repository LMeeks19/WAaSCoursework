from django.shortcuts import render, redirect
from payapp.forms import TransactionForm
from register.models import User
from payapp.models import Transaction, TransactionStatus, TransactionType
from datetime import datetime
from django.db.models import Q


def direct_payments(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = Transaction(
                    sender_email=request.user.email,
                    receiver_email=form.cleaned_data['email'],
                    reference=form.cleaned_data['reference'],
                    amount=form.cleaned_data['amount'],
                    send_date=datetime.utcnow(),
                    status=TransactionStatus.CLEARED,
                    type=TransactionType.DIRECT
                )
                sender = User.objects.get(email=transaction.sender_email)
                receiver = User.objects.get(email=transaction.receiver_email)
                sender.balance = sender.balance - transaction.amount
                receiver.balance = receiver.balance + transaction.amount
                transaction.save()
                sender.save()
                receiver.save()
            return redirect('direct-payment')
        user_direct_payments = list(Transaction.objects.filter(sender_email=request.user.email, type=TransactionType.DIRECT).order_by('-send_date'))
        return render(request, "payapp/direct-payments.html", {"user_direct_payments": user_direct_payments})
    return redirect('unauthorised')


def payment_requests(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = Transaction(
                    sender_email=request.user.email,
                    receiver_email=form.cleaned_data['email'],
                    reference=form.cleaned_data['reference'],
                    amount=form.cleaned_data['amount'],
                    send_date=datetime.utcnow(),
                    status=TransactionStatus.PENDING,
                    type=TransactionType.REQUEST
                )
                sender = User.objects.get(email=transaction.sender_email)
                receiver = User.objects.get(email=transaction.receiver_email)
                sender.balance = sender.balance - transaction.amount
                receiver.balance = receiver.balance + transaction.amount
                transaction.save()
                sender.save()
                receiver.save()
            return redirect('payment-requests')
        user_sent_requests = list(Transaction.objects.filter(sender_email=request.user.email, type=TransactionType.REQUEST).order_by('-send_date'))
        user_received_requests = list(Transaction.objects.filter(receiver_email=request.user.email, type=TransactionType.REQUEST).order_by('-send_date'))
        return render(request, "payapp/payment-requests.html", {"user_received_requests": user_received_requests, "user_sent_requests": user_sent_requests})
    return redirect('unauthorised')


def transactions(request):
    if request.user.is_authenticated:
        user_transactions = list(Transaction.objects.filter(status=TransactionStatus.CLEARED).filter(Q(sender_email=request.user.email) | Q(receiver_email=request.user.email)))
        return render(request, "payapp/transactions.html", {"user_transactions": user_transactions})
    return redirect('unauthorised')


def account(request):
    if request.user.is_authenticated:
        return render(request, "payapp/account.html")
    return redirect('unauthorised')


def admin(request):
    if request.user.is_authenticated:
        all_users = list(User.objects.all().order_by('-is_superuser'))
        all_transactions = list(Transaction.objects.filter(status=TransactionStatus.CLEARED).order_by('-send_date'))
        return render(request, "payapp/admin.html", {"all_users": all_users, "all_transactions": all_transactions})
    return redirect('unauthorised')


def unauthorised(request):
    return render(request, "payapp/unauthorised.html")
