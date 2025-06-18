import json
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
# Se usa 'auth_' para evitar conflictos
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password) # Devuelve User o error
        if user is not None:
            auth_login(request, user) # Establece la cookie de sesión
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Credenciales inválidas'}, status=401)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def api_logout(request):
    if request.method == 'POST':
        auth_logout(request) # Borra la cookie de sesión
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def api_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username') # DNI
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        email = data.get('email', '')
        rol = data.get('rol')

        if not username or not password:
            return JsonResponse({'success': False, 'error': 'Faltan campos obligatorios'}, status=400)
        
        if not username_es_dni(username):
            return JsonResponse({'success': False, 'error': 'El DNI debe ser numérico'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'El usuario ya existe'}, status=400)
        
        if not password_valida(password):
            return JsonResponse({'success': False, 'error': 'La contraseña debe tener al menos 8 caracteres, una letra y un número'}, status=400)
        
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        group, _ = Group.objects.get_or_create(name=rol)
        user.groups.add(group)
        return JsonResponse({'success': True, 'message': 'Usuario creado correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def api_password_change(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not old_password or not new_password:
            return JsonResponse({'success': False, 'error': 'Faltan campos obligatorios'}, status=400)

        user = request.user
        if not user.check_password(old_password):
            return JsonResponse({'success': False, 'error': 'Contraseña antigua incorrecta'}, status=400)

        if not password_valida(new_password):
            return JsonResponse({'success': False, 'error': 'La nueva contraseña debe tener al menos 8 caracteres, una letra y un número'}, status=400)

        user.set_password(new_password)
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def username_es_dni(username):
    checks = {
        'is_string': lambda u: isinstance(u, str),
        'is_numeric': lambda u: u.isdigit(),
        'max_length': lambda u: len(u) <= 10,
    }
    for check in checks.values():
        if not check(username):
            return False
    return True


def password_valida(password):
    if len(password) < 8:
        return False
    tiene_letra = any(c.isalpha() for c in password)
    tiene_numero = any(c.isdigit() for c in password)
    return tiene_letra and tiene_numero
