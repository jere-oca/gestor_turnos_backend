# turnos/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'turnos', views.TurnoViewSet, basename='turno')
router.register(r'especialidades', views.EspecialidadViewSet, basename='especialidad')
router.register(r'medicos', views.MedicoViewSet, basename='medico')
router.register(r'pacientes', views.PacienteViewSet, basename='paciente')

urlpatterns = [
    path('api/', include(router.urls)),
    # Mantener las URLs existentes para la versión web
    path('crear/', views.crear_turno, name='crear_turno'),
    path('listar/', views.listar_turnos, name='listar_turnos'),
    path('eliminar/<int:turno_id>/', views.eliminar_turno, name='eliminar_turno'),
    path('modificar/<int:turno_id>/', views.modificar_turno, name='modificar_turno'),
]
