import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AuthUser, Persona
from django.db import transaction

@csrf_exempt
def persona_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            tipo_usuario = data.get('tipo_usuario')
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            fecha_nacimiento = data.get('fecha_nacimiento')
            direccion = data.get('direccion')
            telefono = data.get('telefono')
            especialidad = data.get('especialidad')
            consultorio = data.get('consultorio')

            if not (username and password and tipo_usuario and nombre and apellido):
                return JsonResponse({'success': False, 'error': 'Faltan campos obligatorios.'}, status=400)

            with transaction.atomic():
                auth_user = AuthUser.objects.create(
                    username=username,
                    password=password  # Asegúrate de guardar el hash si es necesario
                )
                persona = Persona.objects.create(
                    auth_user=auth_user,
                    tipo_usuario=tipo_usuario,
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=fecha_nacimiento,
                    direccion=direccion,
                    telefono=telefono,
                    especialidad=especialidad,
                    consultorio=consultorio
                )
            return JsonResponse({'success': True, 'message': 'Usuario registrado correctamente.'}, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
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
    return JsonResponse({'error': 'Método no permitido'}, status=405)