from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('paciente/', views.paciente_dashboard, name='paciente_dashboard'),
    path('administrativo/', views.admin_dashboard, name='admin_dashboard'),
] 