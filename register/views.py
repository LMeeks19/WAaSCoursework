from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm


def base(request):
    return redirect("login")


def user_registration(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("transactions")
    return render(request, "register/register.html", {"user_registration": form})


def user_login(request):
    form = AuthenticationForm(request, request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("transactions")
    return render(request, "register/login.html", {"user_login": form})


def user_logout(request):
    logout(request)
    return redirect("login")
