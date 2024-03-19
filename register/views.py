from django.shortcuts import render


def register(request):
    return render(request, "register/register.html")


def login(request):
    return render(request, "register/login.html")


def forgot_password(request):
    return render(request, "register/forgot-password.html")
