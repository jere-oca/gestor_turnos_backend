from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/doctor/', views.doctor_register, name='doctor_register'),
    path('register/paciente/', views.pacient_register, name='doctor_register'),
]