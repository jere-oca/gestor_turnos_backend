from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from turnos.models import Turno


def base_dashboard(username):
    turnos = Turno.objects.filter(usuario__username=username)
    data = [{"id": t.id} for t in turnos]
    return data
    
@login_required
def api_dashboard(request):
    if request.user.is_authenticated:
        rol = request.GET.get('rol')
        if rol == 'doctor':
            return doctor_dashboard(request)
        elif rol == 'paciente':
            return paciente_dashboard(request)
        elif rol == 'secretario':
            return secretario_dashboard(request)
        else:
            return JsonResponse({'error': 'Rol no válido'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def doctor_dashboard(request):
    # data = base_dashboard(request.user.username)
    if request.method == 'GET':
        return JsonResponse({'dashboard': 'doctor', 'info': 'Datos del doctor'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def paciente_dashboard(request):
    if request.method == 'GET':
        return JsonResponse({'dashboard': 'paciente', 'info': 'Datos del paciente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def secretario_dashboard(request):
    if request.method == 'GET':
        return JsonResponse({'dashboard': 'secretario', 'info': 'Datos del secretario'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
