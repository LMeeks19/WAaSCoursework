from django.shortcuts import render, redirect
from register.models import User
from payapp.forms import TransactionForm
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
                    receiver_email=form.cleaned_data['receiver_email'],
                    reference=form.cleaned_data['reference'],
                    amount=form.cleaned_data['amount'],
                    send_date=datetime.utcnow(),
                    status=TransactionStatus.PENDING,
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
        form = TransactionForm()
        user_transactions = list(Transaction.objects.filter(sender_email=request.user.email, type=TransactionType.DIRECT).order_by('-send_date'))
        return render(request, "payapp/direct-payments.html", {"direct_payment": form, "user_transactions": user_transactions})
    return redirect('unauthorised')


def payment_requests(request):
    if request.user.is_authenticated:
        return render(request, "payapp/payment-requests.html")
    return redirect('unauthorised')


def transactions(request):
    if request.user.is_authenticated:
        user_transactions = list(Transaction.objects.filter(Q(sender_email=request.user.email) | Q(receiver_email=request.user.email)))
        return render(request, "payapp/transactions.html", {"user_transactions": user_transactions })
    return redirect('unauthorised')


def account(request):
    if request.user.is_authenticated:
        return render(request, "payapp/account.html")
    return redirect('unauthorised')


def admin(request):
    if request.user.is_authenticated:
        all_users = list(User.objects.all().order_by('-is_superuser'))
        all_transactions = list(Transaction.objects.all())
        return render(request, "payapp/admin.html", {"all_users": all_users, "all_transactions": all_transactions})
    return redirect('unauthorised')


def unauthorised(request):
    return render(request, "payapp/unauthorised.html")
