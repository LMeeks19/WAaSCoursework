from django.shortcuts import render


def direct_payments(request):
    return render(request, "payapp/direct-payments.html")


def payment_requests(request):
    return render(request, "payapp/payment-requests.html")


def transactions(request):
    return render(request, "payapp/transactions.html")


def profile(request):
    return render(request, "payapp/profile.html")
