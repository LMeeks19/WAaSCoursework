from django.urls import path
from . import views as payapp_views
from register import views as register_views

urlpatterns = [
    path('transactions/', payapp_views.transactions, name='transactions'),
    path('payment-requests/', payapp_views.payment_requests, name='payment-requests'),
    path('direct-payments/', payapp_views.direct_payments, name='direct-payment'),
    path('profile/', payapp_views.profile, name='profile'),
    path('register/', register_views.register, name='register'),
    path('login/', register_views.login, name='login'),
    path('forgotten-password/', register_views.forgot_password, name='forgotten-password'),
]
