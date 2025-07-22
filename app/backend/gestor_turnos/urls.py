"""
URL configuration for gestor_turnos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from turnos import views as turnos_views
from authentification import views as auth_views

# Router para API
router = DefaultRouter()
router.register(r'turnos', turnos_views.TurnoViewSet, basename='turno')
router.register(r'especialidades', turnos_views.EspecialidadViewSet, basename='especialidad')
router.register(r'medicos', turnos_views.MedicoViewSet, basename='medico')
router.register(r'pacientes', turnos_views.PacienteViewSet, basename='paciente')

urlpatterns = [
    # Opción 1: Redirección directa de la raíz al login
    path('', RedirectView.as_view(url='login/', permanent=False)),
    
    # URLs principales
    path('admin/', admin.site.urls),
    path('dashboards/', include('dashboards.urls')),
    path('turnos/', include('turnos.urls')),
    
    # API endpoints - BEFORE authentification URLs to avoid conflicts
    path('api/', include(router.urls)),
    path('api/login/', auth_views.api_login, name='api_login'),
    path('api/logout/', auth_views.api_logout, name='api_logout'),
    path('api/register/', auth_views.api_register, name='api_register'),
    path('api/csrf/', auth_views.get_csrf, name='get_csrf'),
    path('api/user/', auth_views.user_info_api, name='api_user'),
    
    # URLs de autenticación ahora en la raíz - MUST BE LAST
    path('', include('authentification.urls')),  # Esto incluye login/, register/, etc.
]
