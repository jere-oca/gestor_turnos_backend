# Standard library imports
import json
from datetime import datetime
from functools import wraps

# Django imports
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods, require_safe, require_POST

# Local imports
from .models import AuthUser, Persona
from .forms import AuthUserForm, PersonaForm, CustomAuthenticationForm
from .utils import (
    create_redis_session, 
    set_session_data, 
    get_redis_session, 
    delete_redis_session, 
    authenticate_user_and_create_session
)






@require_safe
def login_form(request):
    """Renderiza el formulario de inicio de sesión."""
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@require_POST
def process_login(request):
    """Procesa el formulario de inicio de sesión web."""
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    form = CustomAuthenticationForm(request, data=request.POST)
    
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Reutilizar función utilitaria para crear sesión Redis
            auth_result = authenticate_user_and_create_session(username, password, request)
            if auth_result['success']:
                request.session['redis_session_key'] = auth_result['redis_session_key']
            
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Error: Credenciales inválidas.')
            return redirect('login')
    else:
        return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas.'})
@login_required
def logout_view(request):
    auth_user_id= request.session.get('auth_user_id')
    if auth_user_id:
        delete_redis_session(auth_user_id)

    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

@require_safe
def register_form(request):
    """Renderiza el formulario de registro."""
    if request.session.get('auth_user_id'):
        return redirect('dashboard_redirect')
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
                # Crear el usuario de autenticación usando el form
                auth_user = auth_form.save()
                
                # Crear la persona
                persona = persona_form.save(commit=False)
                persona.auth_user = auth_user
                persona.save()
            
            messages.success(request, 'Usuario registrado correctamente. Por favor inicia sesión.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
    else:
        messages.error(request, 'Por favor corrige los errores en el formulario.')
    
    return render(request, 'register.html', {
        'auth_form': auth_form,
        'persona_form': persona_form
    })

def api_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('auth_user_id'):
            return JsonResponse({'error': 'No autorizado'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@csrf_exempt
@ensure_csrf_cookie
@require_http_methods(["POST"])
def api_login(request):
    """Procesa el inicio de sesión vía API."""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        print(f"[DEBUG] Datos recibidos: username={username}, password={'***' if password else 'None'}")
        
        # Usar la función utilitaria para autenticar y crear sesión
        auth_result = authenticate_user_and_create_session(username, password, request)
        
        print(f"[DEBUG] auth_result: {auth_result}")
        
        # ⭐ VERIFICAR SI auth_result ES None
        if auth_result is None:
            return JsonResponse({
                'success': False, 
                'error': 'Error interno: auth_result es None'
            }, status=500)
        
        if not auth_result.get('success', False):
            return JsonResponse({
                'success': False, 
                'error': auth_result.get('error', 'Error desconocido')
            }, status=auth_result.get('status', 500))
        
        # ⭐ VERIFICAR SI session_data EXISTE
        session_data = auth_result.get('session_data')
        if session_data is None:
            return JsonResponse({
                'success': False, 
                'error': 'Error: session_data es None'
            }, status=500)
        
        # Establecer datos de sesión en Django
        set_session_data(request, session_data)
        
        # Respuesta exitosa
        return JsonResponse({
            'success': True,
            'message': 'Inicio de sesión exitoso.',
            'tipo_usuario': session_data['tipo_usuario'],
            'nombre': session_data['nombre'],
            'apellido': session_data['apellido'],
            'session_key': session_data['redis_session_key']
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'error': 'JSON inválido'
        }, status=400)
    except Exception as e:
        print(f"[DEBUG] Error en api_login: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)



@api_login_required
@require_http_methods(["POST"])
def api_logout(request):
    """Cierra la sesión del usuario."""

    auth_user_id = request.session.get('auth_user_id')
    if auth_user_id:
        delete_redis_session(auth_user_id)

    logout(request)
    response = JsonResponse({'success': True, 'message': 'Sesión cerrada exitosamente'})
    response.delete_cookie('sessionid')
    return response



# Agregar esta nueva función antes de get_csrf
@api_login_required
@require_http_methods(["GET"])
def api_get_session(request):
    """Obtiene datos de la sesión desde Redis"""
    auth_user_id = request.session.get('auth_user_id')
    if not auth_user_id:
        return JsonResponse({'error': 'Sesión no válida'}, status=401)
    
    redis_data = get_redis_session(auth_user_id)
    if redis_data:
        # Actualizar última actividad
        redis_data['last_activity'] = datetime.now().isoformat()
        session_key = f"user_session:{auth_user_id}"
        cache.set(session_key, json.dumps(redis_data), timeout=86400)
        
        return JsonResponse({
            'success': True,
            'session_data': redis_data
        })
    else:
        return JsonResponse({'error': 'Sesión no encontrada en Redis'}, status=404)


@ensure_csrf_cookie
@require_http_methods(["POST"])
def api_register(request):
    """Procesa el registro de un nuevo usuario vía API."""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        tipo_usuario = data.get('tipo_usuario')
        
        if not all([username, password, nombre, apellido, tipo_usuario]):
            return JsonResponse({
                'success': False,
                'error': 'Todos los campos son requeridos'
            }, status=400)
        
        try:
            with transaction.atomic():
                # Crear el usuario de autenticación
                auth_user = AuthUser.objects.create_user(
                    username=username,
                    password=password  # En producción usar hash
                )
                
                # Crear la persona
                Persona.objects.create(
                    auth_user=auth_user,
                    nombre=nombre,
                    apellido=apellido,
                    tipo_usuario=tipo_usuario
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Usuario registrado correctamente'
            }, status=201)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al registrar usuario: {str(e)}'
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@ensure_csrf_cookie
def get_csrf(request):
    """
    Esta vista devuelve una respuesta simple con un token CSRF.
    Usa @ensure_csrf_cookie para forzar al navegador a establecer la cookie CSRF.
    """
    return JsonResponse({'success': True, 'message': 'CSRF cookie set'})