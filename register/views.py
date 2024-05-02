from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.db import transaction, OperationalError


# Redirects the user to the login page if they don't initially type /login into the url
def base(request):
    return redirect("/webapps2024/login/")


# Registration page view
def user_registration(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        try:
            with transaction.atomic():
                if form.is_valid():
                    user = form.save()
                    login(request, user)
                    return redirect('transactions')
        except OperationalError:
            redirect('register')
    return render(request, "register/register.html", {"user_registration_form": form})


# Login page view
def user_login(request):
    logout(request)
    form = AuthenticationForm(request, request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("transactions")
    return render(request, "register/login.html", {"user_login_form": form})


# View for when a user logs out
def user_logout(request):
    logout(request)
    return redirect("login")


# Unauthorised page view
def unauthorised(request):
    return render(request, "register/unauthorised.html")


# Not Found page view
def not_found(request, exception):
    return render(request, "register/not-found.html", status=404)



