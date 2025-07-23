from django.core.management.base import BaseCommand
from django.db import transaction
from authentification.models import AuthUser, Persona
from turnos.models import Especialidad, Medico, Paciente
from datetime import datetime

class Command(BaseCommand):
    help = 'Crea usuarios de prueba para testing'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Creando usuarios de prueba...")
        
        # Crear usuarios de prueba
        usuarios_prueba = [
            {
                'username': 'melisahernandez',
                'password': 'T_0SDlq9)n0N',
                'tipo': 'paciente'
            },
            {
                'username': 'doctor1', 
                'password': 'test123',
                'tipo': 'doctor'
            },
            {
                'username': 'admin1',
                'password': 'test123', 
                'tipo': 'administrativo'
            }
        ]
        
        try:
            with transaction.atomic():
                # Crear especialidad si no existe
                especialidad, created = Especialidad.objects.get_or_create(
                    nombre="Medicina General",
                    defaults={'descripcion': "Especialidad general"}
                )
                if created:
                    self.stdout.write(f" Especialidad creada: {especialidad.nombre}")
                
                for user_data in usuarios_prueba:
                    # Crear AuthUser
                    auth_user, created = AuthUser.objects.get_or_create(
                        username=user_data['username'],
                        defaults={
                            'is_active': True,
                            'is_staff': False,
                            'is_superuser': False
                        }
                    )
                    
                    if created:
                        auth_user.set_password(user_data['password'])
                        auth_user.save()
                        self.stdout.write(f" Usuario creado: {auth_user.username}")
                    else:
                        self.stdout.write(f"ℹ  Usuario ya existe: {auth_user.username}")
                    
                    # Definir nombres específicos
                    if user_data['username'] == 'melisahernandez':
                        nombre = "Melisa"
                        apellido = "Hernandez"
                    else:
                        nombre = f"Nombre {auth_user.username}"
                        apellido = f"Apellido {auth_user.username}"
                    
                    # Crear Persona
                    persona, created = Persona.objects.get_or_create(
                        auth_user=auth_user,
                        defaults={
                            'tipo_usuario': user_data['tipo'],
                            'nombre': nombre,
                            'apellido': apellido,
                            'telefono': "000-000-0000"
                        }
                    )
                    
                    if created:
                        self.stdout.write(f" Persona creada: {persona.nombre} ({persona.tipo_usuario})")
                    else:
                        self.stdout.write(f" Persona ya existe: {persona.nombre} ({persona.tipo_usuario})")
                    
                    # Crear registros específicos según el tipo
                    if user_data['tipo'] == 'paciente':
                        paciente, created = Paciente.objects.get_or_create(
                            user=auth_user,
                            defaults={
                                'dni': f"DNI{auth_user.id:06d}",
                                'fecha_nacimiento': "1990-01-01",
                                'telefono': "000-000-0000",
                                'direccion': f"Dirección de {auth_user.username}"
                            }
                        )
                        if created:
                            self.stdout.write(f" Paciente creado: {paciente.dni}")
                    
                    elif user_data['tipo'] == 'doctor':
                        medico, created = Medico.objects.get_or_create(
                            user=auth_user,
                            defaults={
                                'especialidad': especialidad,
                                'matricula': f"MAT{auth_user.id:06d}",
                                'telefono': "000-000-0000"
                            }
                        )
                        if created:
                            self.stdout.write(f" Médico creado: {medico.matricula}")
                
                self.stdout.write("\n Usuarios de prueba creados exitosamente!")
                self.stdout.write("\nUsuarios disponibles:")
                for user_data in usuarios_prueba:
                    self.stdout.write(f"  {user_data['username']} ({user_data['tipo']}) - Password: {user_data['password']}")
                
        except Exception as e:
            self.stdout.write(f" Error: {e}")
            import traceback
            self.stdout.write(traceback.format_exc())
