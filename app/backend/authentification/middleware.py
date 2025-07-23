from django.utils.deprecation import MiddlewareMixin
from authentification.models import AuthUser

class CustomAuthMiddleware(MiddlewareMixin):
    """
    Middleware para establecer request.user basado en nuestra autenticación personalizada
    """
    def process_request(self, request):
        # Solo procesar rutas de API
        if not request.path.startswith('/api/'):
            return None
            
        # Obtener el auth_user_id de la sesión
        auth_user_id = request.session.get('auth_user_id')
        
        if auth_user_id:
            try:
                # Buscar el usuario en nuestra tabla personalizada
                auth_user = AuthUser.objects.get(id=auth_user_id)
                request.user = auth_user
                request.user.is_authenticated = True
            except AuthUser.DoesNotExist:
                # Si no existe el usuario, establecer como anónimo
                from django.contrib.auth.models import AnonymousUser
                request.user = AnonymousUser()
        else:
            # Si no hay auth_user_id en la sesión, usuario anónimo
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()
        
        return None
