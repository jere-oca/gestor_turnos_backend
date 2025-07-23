import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authentification.models import Persona  # Ajusta si tu modelo Persona está en otro lugar    
class Command(BaseCommand):
    help = 'Importa usuarios y personas desde archivos CSV relacionados.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=str,
            default='csv_exports/auth_users.csv',
            help='Ruta al archivo CSV de usuarios.'
        )
        parser.add_argument(
            '--personas',
            type=str,
            default='csv_exports/personas.csv',
            help='Ruta al archivo CSV de personas.'
        )

    def handle(self, *args, **options):
        User = get_user_model()
        users_path = options['users']
        personas_path = options['personas']

        # 1. Leer solo los primeros 100 usuarios y crear un diccionario {id: (username, password)}
        users_dict = {}
        with open(users_path, newline='', encoding='utf-8') as usersfile:
            reader = csv.DictReader(usersfile)
            for row in reader:
                users_dict[row['id']] = {
                    'username': row['username'],
                    'password': row['password']
                }

        # 2. Crear usuarios en la base de datos y mapear por id
        user_objs = {}
        for user_id, data in users_dict.items():
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={'is_active': True}
            )
            if created:
                user.set_password(data['password'])
                user.save()
            user_objs[user_id] = user

        # 3. Leer solo las primeras 100 personas y asociar con usuarios por id
        with open(personas_path, newline='', encoding='utf-8') as personasfile:
            reader = csv.DictReader(personasfile)
            for row in reader:
                user = user_objs.get(row['auth_user_id'])
                if not user:
                    self.stdout.write(self.style.WARNING(f"Usuario con id {row['auth_user_id']} no encontrado. Saltando persona."))
                    continue
                especialidad_nombre = row.get('especialidad')
                especialidad = None
                if especialidad_nombre and especialidad_nombre.strip().lower() not in ['null', 'none', '']:
                    especialidad = especialidad_nombre.strip()
                Persona.objects.get_or_create(
                    auth_user=user,
                    defaults={
                        'tipo_usuario': row['tipo_usuario'],
                        'nombre': row['nombre'],
                        'apellido': row['apellido'],
                        'fecha_nacimiento': row['fecha_nacimiento'],
                        'direccion': row['direccion'],
                        'telefono': row['telefono'],
                        'especialidad': especialidad,
                        'consultorio': row['consultorio'] if row['consultorio'] else None
                    }
                )
        self.stdout.write(self.style.SUCCESS('Importación de usuarios y personas completada.'))