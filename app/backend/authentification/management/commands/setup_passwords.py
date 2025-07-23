from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from authentification.models import AuthUser


class Command(BaseCommand):
    help = 'Hashea las contraseñas de los usuarios cargados por fixtures'

    def handle(self, *args, **options):
        self.stdout.write('[SETUP] Verificando y hasheando contraseñas de usuarios...')
        
        # Mapeo de usuarios y sus contraseñas de texto plano
        user_passwords = {
            'admin': 'admin123',
            'medico1': 'medico123', 
            'paciente1': 'paciente123'
        }
        
        for username, plain_password in user_passwords.items():
            try:
                user = AuthUser.objects.get(username=username)
                
                # Verificar si la contraseña ya está hasheada
                if user.check_password(plain_password):
                    self.stdout.write(f'✅ {username}: contraseña ya hasheada correctamente')
                    continue
                
                # Si no está hasheada, hashearla
                user.password = make_password(plain_password)
                user.save()
                self.stdout.write(f'🔧 {username}: contraseña hasheada y guardada')
                
            except AuthUser.DoesNotExist:
                self.stdout.write(f'  {username}: usuario no encontrado, omitiendo...')
                continue
        
        self.stdout.write('[SETUP]  Verificación de contraseñas completada')
