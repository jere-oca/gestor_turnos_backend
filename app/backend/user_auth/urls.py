from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="api_login/", permanent=False)),
    path("login/", views.api_login, name="api_login"),
    path("logout/", views.api_logout, name="api_logout"),
    path("register/", views.api_register, name="api_register"),
    path("password_change/", views.api_password_change, name="api_password_change"),
    ]
