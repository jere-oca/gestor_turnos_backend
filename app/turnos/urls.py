# turnos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_turno, name='crear_turno'),
    path('', views.listar_turnos, name='listar_turnos'),
]
