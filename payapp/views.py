from django.shortcuts import render, redirect
from payapp.forms import DirectPaymentForm, PaymentRequestForm
from .server import get_all_cleared_transaction, get_user_sent_direct_payments, get_all_users, get_user_sent_payment_requests, get_user_received_payment_requests, get_user_cleared_transactions, get_transaction, get_user
from .transaction import create_direct_payment, create_payment_request, accept_payment_request, reject_payment_request
from django.contrib import messages


def direct_payments(request):
    if request.user.is_authenticated:
        form = DirectPaymentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                create_direct_payment(sender_email=request.user.email, receiver_email=form.cleaned_data.get('receiver_email'), reference=form.cleaned_data.get('reference'), amount=form.cleaned_data.get('amount'))
                return redirect('direct-payments')
        user_direct_payments = get_user_sent_direct_payments(request.user.email)
        return render(request, "payapp/direct-payments.html",
                      {"user_direct_payments": user_direct_payments, "direct_payment_form": form})
    return redirect('unauthorised')


def payment_requests(request):
    if request.user.is_authenticated:
        form = PaymentRequestForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                create_payment_request(sender_email=request.user.email, receiver_email=form.cleaned_data.get('receiver_email'), reference=form.cleaned_data.get('reference'), amount=form.cleaned_data.get('amount'))
                return redirect('payment-requests')
        user_sent_requests = get_user_sent_payment_requests(request.user.email)
        user_received_requests = get_user_received_payment_requests(request.user.email)
        return render(request, "payapp/payment-requests.html", {"user_received_requests": user_received_requests, "user_sent_requests": user_sent_requests, "payment_requests_form": form})
    return redirect('unauthorised')


def payment_request_accept(request):
    if request.method == "GET":
        transaction_id = request.GET.get("transaction_id")
        transaction = get_transaction(transaction_id)
        user = get_user(request.GET.get("user_id"))
        if user.balance >= transaction.amount:
            accept_payment_request(transaction_id)
        else:
            messages.error(request, "You do not possess the required funds to accepts this payment request")
    return redirect('payment-requests')


def payment_request_reject(request):
    if request.method == "GET":
        transaction_id = request.GET.get("id")
        reject_payment_request(transaction_id)
    return redirect('payment-requests')


def transactions(request):
    if request.user.is_authenticated:
        user_transactions = get_user_cleared_transactions(request.user.email)
        return render(request, "payapp/transactions.html", {"user_transactions": user_transactions})
    return redirect('unauthorised')


def account(request):
    if request.user.is_authenticated:
        return render(request, "payapp/account.html")
    return redirect('unauthorised')


def admin(request):
    if request.user.is_authenticated:
        all_users = get_all_users()
        all_transactions = get_all_cleared_transaction()
        return render(request, "payapp/admin.html", {"all_users": all_users, "all_transactions": all_transactions})
    return redirect('unauthorised')


def unauthorised(request):
    return render(request, "payapp/unauthorised.html")
