from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm


def base(request):
    return redirect("login")


def user_registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    form = RegisterForm()
    return render(request, "register/register.html", {"user_registration": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "payapp/transactions.html")
    form = AuthenticationForm()
    return render(request, "register/login.html", {"user_login": form})


def user_logout(request):
    logout(request)
    return redirect("login")
