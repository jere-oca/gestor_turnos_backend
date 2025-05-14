import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AuthUser, Persona
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AuthUserForm, PersonaForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_safe, require_POST

@require_safe
def login_form(request):
    """Renderiza el formulario de inicio de sesión."""
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@require_POST
def process_login(request):
    """Procesa el formulario de inicio de sesión web."""
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        # Aquí puedes autenticar y loguear al usuario si lo deseas
        return render(request, 'login.html', {'form': form, 'success': True})
    else:
        return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas.'})

@require_safe
def register_form(request):
    """Renderiza el formulario de registro."""
    auth_form = AuthUserForm()
    persona_form = PersonaForm()
    return render(request, 'register.html', {
        'auth_form': auth_form,
        'persona_form': persona_form
    })

@require_POST
def process_register(request):
    """Procesa la solicitud de registro de un nuevo usuario."""
    auth_form = AuthUserForm(request.POST)
    persona_form = PersonaForm(request.POST)
    
    if auth_form.is_valid() and persona_form.is_valid():
        try:
            with transaction.atomic():
                # Crear el usuario de autenticación
                auth_user = auth_form.save(commit=False)
                # Aquí deberías hashear la contraseña en un entorno de producción
                auth_user.save()
                
                # Crear la persona
                persona = persona_form.save(commit=False)
                persona.auth_user = auth_user
                persona.save()
            
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
    else:
        messages.error(request, 'Por favor corrige los errores en el formulario.')
    
    # Si hay errores, volvemos a mostrar el formulario con los datos ingresados
    return render(request, 'register.html', {
        'auth_form': auth_form,
        'persona_form': persona_form
    })

@require_POST
@csrf_exempt
def api_login(request):
    """Procesa el inicio de sesión vía API."""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        try:
            auth_user = AuthUser.objects.get(username=username)
            if auth_user.password == password:  # Si usas hash, compara con check_password
                persona = Persona.objects.get(auth_user=auth_user)
                return JsonResponse({
                    'success': True,
                    'message': 'Inicio de sesión exitoso.',
                    'tipo_usuario': persona.tipo_usuario,
                    'nombre': persona.nombre,
                    'apellido': persona.apellido
                }, status=200)
            else:
                return JsonResponse({'success': False, 'error': 'Credenciales inválidas.'}, status=401)
        except AuthUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
