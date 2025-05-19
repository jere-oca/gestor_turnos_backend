import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AuthUser, Persona
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AuthUserForm, PersonaForm, CustomAuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from functools import wraps
from django.contrib.auth import logout

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('auth_user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@require_safe
def login_form(request):
    """Renderiza el formulario de inicio de sesión."""
    if request.session.get('auth_user_id'):
        return redirect('dashboard_redirect')
    form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@require_POST
def process_login(request):
    """Procesa el formulario de inicio de sesión web."""
    if request.session.get('auth_user_id'):
        return redirect('dashboard_redirect')
        
    form = CustomAuthenticationForm(data=request.POST)
    
    if form.is_valid():
        auth_user = form.get_user()
        try:
            persona = Persona.objects.get(auth_user=auth_user)
            
            # Guardar datos en la sesión
            request.session['auth_user_id'] = auth_user.id
            request.session['username'] = auth_user.username
            request.session['tipo_usuario'] = persona.tipo_usuario
            request.session['nombre'] = persona.nombre
            request.session['apellido'] = persona.apellido
            
            # Redirigir al dashboard correspondiente
            return redirect('dashboard_redirect')
            
        except Persona.DoesNotExist as e:
            messages.error(request, 'Error: No se encontró la información del usuario.')
            return redirect('login')
    else:
        return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas.'})

@login_required
def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('sessionid')  # Elimina la cookie de sesión
    return response

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
                # Crear el usuario de autenticación
                auth_user = auth_form.save(commit=False)
                auth_user.save()
                
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
            if auth_user.password == password:  # En producción usar hash
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
        return JsonResponse({'success': False, 'error': str(e)}, status=500)