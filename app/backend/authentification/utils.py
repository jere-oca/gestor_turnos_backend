from datetime import datetime
from django.core.cache import cache
import json as json_module
import json
from django.contrib.auth.hashers import make_password, check_password


def create_redis_session(auth_user, persona, request=None):
    """Crear sesión de usuario en Redis"""
    print(f"[DEBUG] === CREAR SESIÓN REDIS ===")
    print(f"[DEBUG] Usuario: {auth_user.username}, ID: {auth_user.id}")
    
    session_key = f"user_session:{auth_user.id}"
    print(f"[DEBUG] Session key: {session_key}")
    
    session_data = {
        'auth_user_id': auth_user.id,
        'username': auth_user.username,
        'nombre': persona.nombre,
        'apellido': persona.apellido,
        'tipo_usuario': persona.tipo_usuario,
        'login_time': datetime.now().isoformat(),
        'last_activity': datetime.now().isoformat(),
    }
    
    if request:
        session_data['ip_address'] = request.META.get('REMOTE_ADDR')
        session_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
    
    print(f"[DEBUG] Datos a guardar: {session_data}")
    
    try:
        print(f"[DEBUG] Intentando guardar en cache...")
        
        # Verificar que cache esté disponible
        from django.core.cache import cache
        print(f"[DEBUG] Cache backend: {cache.__class__.__name__}")
        
        # Guardar en Redis
        cache.set(session_key, json.dumps(session_data), timeout=86400)
        print(f"[DEBUG] ✅ cache.set() ejecutado")
        
        # Verificar inmediatamente
        test_data = cache.get(session_key)
        print(f"[DEBUG] Verificación inmediata: {test_data}")
        print(f"[DEBUG] Tipo de dato: {type(test_data)}")
        
        if test_data:
            print(f"[DEBUG] ✅ Sesión confirmada en Redis")
            # Verificar que sea JSON válido
            try:
                parsed = json.loads(test_data)
                print(f"[DEBUG] JSON parseado correctamente: {parsed.get('username')}")
            except:
                print(f"[DEBUG] ❌ Error al parsear JSON")
        else:
            print(f"[DEBUG] ❌ Sesión NO se guardó en Redis")
            
    except Exception as e:
        print(f"[DEBUG] ❌ Error al guardar en Redis: {e}")
        import traceback
        traceback.print_exc()
    
    return session_key

def get_redis_session(auth_user_id):
    """Obtener sesión desde Redis"""
    session_key = f"user_session:{auth_user_id}"
    session_data = cache.get(session_key)
    if session_data:
        return json_module.loads(session_data)
    return None

def delete_redis_session(auth_user_id):
    """Eliminar sesión de Redis"""
    session_key = f"user_session:{auth_user_id}"
    cache.delete(session_key)

def authenticate_user_and_create_session(username, password, request=None):
    """
    Autentica usuario y crea sesión en Redis.
    """
    try:
        from .models import AuthUser, Persona
        print(f"[DEBUG] === INICIO AUTENTICACIÓN ===")
        print(f"[DEBUG] Username: {username}")
        print(f"[DEBUG] Password recibido: {'SÍ' if password else 'NO'}")

        # 1. Buscar credenciales en Redis (cache)
        cache_key = f"user_credentials:{username}"
        cached_data = cache.get(cache_key)
        if cached_data:
            try:
                cached = json_module.loads(cached_data)
                print(f"[DEBUG] Cache hit para {username}: {cached}")
                # Verificar contraseña (guardada como texto plano en cache)
                if check_password(password,cached.get('password_hash')):
                    print(f"[DEBUG] ✅ Contraseña correcta (cache) para: {username}")
                    # Simular objetos mínimos para compatibilidad
                    class DummyAuthUser:
                        def __init__(self, id, username):
                            self.id = id
                            self.username = username
                    class DummyPersona:
                        def __init__(self, nombre, apellido, tipo_usuario):
                            self.nombre = nombre
                            self.apellido = apellido
                            self.tipo_usuario = tipo_usuario
                    auth_user = DummyAuthUser(cached['auth_user_id'], username)
                    persona = DummyPersona(cached['nombre'], cached['apellido'], cached['tipo_usuario'])
                    redis_session_key = create_redis_session(auth_user, persona, request)
                    return {
                        'success': True,
                        'auth_user': auth_user,
                        'persona': persona,
                        'redis_session_key': redis_session_key,
                        'session_data': {
                            'auth_user_id': auth_user.id,
                            'username': auth_user.username,
                            'tipo_usuario': persona.tipo_usuario,
                            'nombre': persona.nombre,
                            'apellido': persona.apellido,
                            'redis_session_key': redis_session_key
                        }
                    }
                else:
                    print(f"[DEBUG] ❌ Contraseña incorrecta (cache) para: {username}")
                    return {
                        'success': False,
                        'error': 'Credenciales inválidas.',
                        'status': 401
                    }
            except Exception as e:
                print(f"[DEBUG] ❌ Error al leer cache: {e}")

        # 2. Si no está en cache, buscar en la base de datos
        try:
            auth_user = AuthUser.objects.get(username=username)
        except AuthUser.DoesNotExist:
            print(f"[DEBUG] ❌ Usuario no encontrado: {username}")
            return {
                'success': False,
                'error': 'Usuario no encontrado.',
                'status': 404
            }

        if not auth_user.check_password(password):
            print(f"[DEBUG] ❌ Contraseña incorrecta para: {username}")
            return {
                'success': False,
                'error': 'Credenciales inválidas.',
                'status': 401
            }

        print(f"[DEBUG] ✅ Contraseña correcta para: {username}")
        try:
            persona = Persona.objects.get(auth_user=auth_user)
        except Persona.DoesNotExist:
            print(f"[DEBUG] ❌ Persona no encontrada para usuario: {username}")
            return {
                'success': False,
                'error': 'Datos de persona no encontrados.',
                'status': 404
            }

        # 3. Guardar credenciales en Redis (cache)

        print(f"[DEBUG] Guardando en Redis: username='{username}', cache_key='{cache_key}'")
        cache_data = {
            'auth_user_id': auth_user.id,
            'username': auth_user.username,
            'nombre': persona.nombre,
            'apellido': persona.apellido,
            'tipo_usuario': persona.tipo_usuario,
            'password_hash': make_password(password) # ⚠️ En producción NO guardar contraseñas en texto plano
        }
        cache.set(cache_key, json_module.dumps(cache_data), timeout=86400)
        print(f"[DEBUG] Credenciales guardadas en cache para {username}")

        # 4. Crear sesión en Redis
        redis_session_key = create_redis_session(auth_user, persona, request)
        print(f"[DEBUG] Redis session key retornado: {redis_session_key}")

        return {
            'success': True,
            'auth_user': auth_user,
            'persona': persona,
            'redis_session_key': redis_session_key,
            'session_data': {
                'auth_user_id': auth_user.id,
                'username': auth_user.username,
                'tipo_usuario': persona.tipo_usuario,
                'nombre': persona.nombre,
                'apellido': persona.apellido,
                'redis_session_key': redis_session_key
            }
        }

    except Exception as e:
        print(f"[DEBUG] ❌ Error en autenticación: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'status': 500
        }
    

def set_session_data(request, session_data):
    """
    Establece los datos de sesión en Django session.
    """
    request.session['auth_user_id'] = session_data['auth_user_id']
    request.session['username'] = session_data['username']
    request.session['tipo_usuario'] = session_data['tipo_usuario']
    request.session['nombre'] = session_data['nombre']
    request.session['apellido'] = session_data['apellido']
    request.session['redis_session_key'] = session_data['redis_session_key']