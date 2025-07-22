# turnos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URLs para la versión web
    path('crear/', views.crear_turno, name='crear_turno'),
    path('listar/', views.listar_turnos, name='listar_turnos'),
    path('eliminar/<int:turno_id>/', views.eliminar_turno, name='eliminar_turno'),
    path('modificar/<int:turno_id>/', views.modificar_turno, name='modificar_turno'),
]
