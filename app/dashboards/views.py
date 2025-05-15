from django.shortcuts import render, redirect
from django.contrib import messages
from authentification.views import login_required
from authentification.models import Persona

def dashboard_redirect(request):
    """Redirige al dashboard correspondiente según el tipo de usuario."""
    tipo_usuario = request.session.get('tipo_usuario')
    if tipo_usuario == 'doctor':
        return redirect('doctor_dashboard')
    elif tipo_usuario == 'paciente':
        return redirect('paciente_dashboard')
    elif tipo_usuario == 'administrativo':
        return redirect('admin_dashboard')
    return redirect('login')

@login_required
def doctor_dashboard(request):
    """Dashboard para doctores."""
    if request.session.get('tipo_usuario') != 'doctor':
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('dashboard_redirect')
    
    context = {
        'nombre': request.session.get('nombre'),
        'apellido': request.session.get('apellido'),
        'tipo_usuario': 'Doctor'
    }
    return render(request, 'dashboards/doctor_dashboard.html', context)

@login_required
def paciente_dashboard(request):
    """Dashboard para pacientes."""
    if request.session.get('tipo_usuario') != 'paciente':
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('dashboard_redirect')
    
    context = {
        'nombre': request.session.get('nombre'),
        'apellido': request.session.get('apellido'),
        'tipo_usuario': 'Paciente'
    }
    return render(request, 'dashboards/paciente_dashboard.html', context)

@login_required
def admin_dashboard(request):
    """Dashboard para administrativos."""
    if request.session.get('tipo_usuario') != 'administrativo':
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('dashboard_redirect')
    
    context = {
        'nombre': request.session.get('nombre'),
        'apellido': request.session.get('apellido'),
        'tipo_usuario': 'Administrativo'
    }
    return render(request, 'dashboards/admin_dashboard.html', context)
