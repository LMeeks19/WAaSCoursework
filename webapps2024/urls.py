"""
URL configuration for webapps2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from register import views as register_views
from payapp import views as payapp_views


urlpatterns = [
    path('webapps2024/siteAdmin/', admin.site.urls),
    path('webapps2024/', register_views.base),
    path('webapps2024/transactions/', payapp_views.transactions, name='transactions'),
    path('webapps2024/payment-requests/', payapp_views.payment_requests, name='payment-requests'),
    path('webapps2024/direct-payments/', payapp_views.direct_payments, name='direct-payment'),
    path('webapps2024/admin/', payapp_views.admin, name='admin'),
    path('webapps2024/account/', payapp_views.account, name='account'),
    path('webapps2024/register/', register_views.user_registration, name='register'),
    path('webapps2024/login/', register_views.user_login, name='login'),
    path('webapps2024/logout/', register_views.user_logout, name='logout'),
    path('webapps2024/unauthorised/', payapp_views.unauthorised, name='unauthorised')
]
