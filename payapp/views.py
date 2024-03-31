from django.shortcuts import render, redirect
from register.models import User


def direct_payments(request):
    if request.user.is_authenticated:
        return render(request, "payapp/direct-payments.html")
    return redirect('unauthorised')


def payment_requests(request):
    if request.user.is_authenticated:
        return render(request, "payapp/payment-requests.html")
    return redirect('unauthorised')


def transactions(request):
    if request.user.is_authenticated:
        return render(request, "payapp/transactions.html")
    return redirect('unauthorised')


def account(request):
    if request.user.is_authenticated:
        return render(request, "payapp/account.html")
    return redirect('unauthorised')


def admin(request):
    if request.user.is_authenticated:
        users = list(User.objects.all())
        return render(request, "payapp/admin.html", {"users": users})
    return redirect('unauthorised')


def unauthorised(request):
    return render(request, "payapp/unauthorised.html")
