from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_dashboard, name='dashboard_redirect'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('paciente/', views.paciente_dashboard, name='paciente_dashboard'),
    path('secretario/', views.secretario_dashboard, name='secretario_dashboard'),
]