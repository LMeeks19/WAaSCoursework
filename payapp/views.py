from django.shortcuts import render, redirect
from payapp.forms import DirectPaymentForm, PaymentRequestForm
from .server import get_all_user_transactions, get_user_sent_direct_payments, get_all_users, \
    get_user_sent_payment_requests, get_user_received_payment_requests, get_user_cleared_transactions, get_transaction, \
    get_user
from .transaction import create_direct_payment, create_payment_request, accept_payment_request, reject_payment_request
from django.contrib import messages
from django.db import transaction, OperationalError
from register.forms import RegisterForm
from register.models import User
from webapps2024.settings import DEBUG


def direct_payments(request):
    if request.user.is_authenticated:
        form = DirectPaymentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                try:
                    with transaction.atomic():
                        create_direct_payment(sender_email=request.user.email,
                                              receiver_email=form.cleaned_data.get('receiver_email'),
                                              reference=form.cleaned_data.get('reference'),
                                              amount=form.cleaned_data.get('amount'))
                        messages.success(request,
                                         'Direct Payment sent to {0}'.format(form.cleaned_data.get('receiver_email')))
                except OperationalError:
                    messages.error(request, "Unable to send Direct Payment of this amount anymore")
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
                create_payment_request(sender_email=request.user.email,
                                       receiver_email=form.cleaned_data.get('receiver_email'),
                                       reference=form.cleaned_data.get('reference'),
                                       amount=form.cleaned_data.get('amount'))
                messages.success(request, 'Payment Request sent to {0}'.format(form.cleaned_data.get('receiver_email')))
                return redirect('payment-requests')
        user_sent_requests = get_user_sent_payment_requests(request.user.email)
        user_received_requests = get_user_received_payment_requests(request.user.email)
        return render(request, "payapp/payment-requests.html", {"user_received_requests": user_received_requests, "user_sent_requests": user_sent_requests, "payment_requests_form": form})
    return redirect('unauthorised')


def payment_request_accept(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            transaction_id = request.GET.get("transaction_id")
            retrieved_transaction = get_transaction(transaction_id)
            user = get_user(request.GET.get("user_id"))
            if user.balance >= retrieved_transaction.receiver_amount:
                try:
                    with transaction.atomic():
                        accept_payment_request(retrieved_transaction.id)
                        messages.info(request, 'Payment Request fulfilled')
                except OperationalError:
                    messages.error(request, "Unable to accept this Payment Request anymore")
            else:
                messages.error(request, "You do not possess the required funds to accepts this payment request")
        return redirect('payment-requests')
    return redirect('unauthorised')


def payment_request_reject(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            transaction_id = request.GET.get("id")
            reject_payment_request(transaction_id)
            messages.info(request, 'Payment Request rejected')
        return redirect('payment-requests')
    return redirect('unauthorised')


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
        if request.user.is_superuser:
            all_users = get_all_users()
            return render(request, "payapp/admin.html", {"all_users": all_users, "dev_window_active": DEBUG})
        else:
            messages.info(request, 'You do not have access to this page')
            return redirect('transactions')
    return redirect('unauthorised')


def admin_create_user(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            form = RegisterForm(request.POST or None)
            if request.method == "POST":
                try:
                    with transaction.atomic():
                        if form.is_valid():
                            is_admin = request.POST.get('admin') == "yes"
                            user = User(username=form.cleaned_data.get('username'),
                                        first_name=form.cleaned_data.get('first_name'),
                                        last_name=form.cleaned_data.get('last_name'),
                                        email=form.cleaned_data.get('email'),
                                        phone_number=form.cleaned_data.get('phone_number'),
                                        currency=form.cleaned_data.get('currency'),
                                        password=form.cleaned_data.get('password1'),
                                        )
                            if is_admin:
                                user.create_admin()
                                messages.success(request, "Admin: {0} created".format(user.username))
                            else:
                                user.create_user()
                                messages.success(request, "User: {0} created".format(user.username))
                        return redirect('admin')
                except OperationalError:
                    messages.error(request, "Unable to create this user/admin anymore")
            return render(request, "payapp/admin-create-user.html", {"create_user_form": form})
        else:
            messages.info(request, 'You do not have access to this page')
            return redirect('transactions')
    return redirect('unauthorised')


def admin_view_user(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = get_user(user_id=id)
            user_transactions = get_all_user_transactions(user_email=user.email)
            return render(request, "payapp/admin-view-user.html",
                          {"selected_user": user, "user_transactions": user_transactions})
        else:
            messages.info(request, 'You do not have access to this page')
            return redirect('transactions')
    return redirect('unauthorised')


def change_admin_status(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = get_user(user_id=id)
            try:
                with transaction.atomic():
                    user.is_superuser = not user.is_superuser
                    user.is_staff = not user.is_staff
                    user.save()
                    messages.info(request, 'Admin status updated for {0}'.format(user.username))
                    return redirect('/webapps2024/admin/view/{0}'.format(user.id))
            except OperationalError:
                messages.info(request, 'Unable to update admin status for {0}'.format(user.username))
        else:
            messages.info(request, 'You do not have access to this page')
            return redirect('transactions')
    return redirect('unauthorised')