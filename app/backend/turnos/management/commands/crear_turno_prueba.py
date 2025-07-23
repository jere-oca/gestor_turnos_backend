from django.core.management.base import BaseCommand
from django.db import transaction
from authentification.models import AuthUser, Persona
from turnos.models import Turno, Paciente, Medico
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Crea un turno de prueba para testing'

    def add_arguments(self, parser):
        parser.add_argument('--paciente', type=str, help='Username del paciente')
        parser.add_argument('--medico', type=str, help='Username del médico')

    def handle(self, *args, **options):
        paciente_username = options.get('paciente', 'miguel62')  # Usuario paciente por defecto
        medico_username = options.get('medico', 'belen16')      # Usuario médico por defecto
        
        try:
            # Buscar el usuario paciente
            auth_user_paciente = AuthUser.objects.get(username=paciente_username)
            persona_paciente = Persona.objects.get(auth_user=auth_user_paciente)
            
            if persona_paciente.tipo_usuario != 'paciente':
                self.stdout.write(f"❌ Error: {paciente_username} no es un paciente")
                return
            
            # Buscar el usuario médico
            auth_user_medico = AuthUser.objects.get(username=medico_username)
            persona_medico = Persona.objects.get(auth_user=auth_user_medico)
            
            if persona_medico.tipo_usuario != 'doctor':
                self.stdout.write(f"❌ Error: {medico_username} no es un médico")
                return
            
            # Obtener o crear el registro de Paciente
            try:
                paciente = Paciente.objects.get(user=auth_user_paciente)
            except Paciente.DoesNotExist:
                paciente = Paciente.objects.create(
                    user=auth_user_paciente,
                    dni=f"DNI-{auth_user_paciente.id}",
                    fecha_nacimiento="1990-01-01",
                    telefono="000-000-0000",
                    direccion="Dirección de prueba"
                )
                self.stdout.write(f"✅ Creado registro de Paciente para {paciente_username}")
            
            # Obtener o crear el registro de Médico
            try:
                medico = Medico.objects.get(user=auth_user_medico)
            except Medico.DoesNotExist:
                # Importar Especialidad
                from turnos.models import Especialidad
                try:
                    especialidad = Especialidad.objects.first()
                    if not especialidad:
                        especialidad = Especialidad.objects.create(
                            nombre="Medicina General",
                            descripcion="Especialidad general"
                        )
                except:
                    especialidad = None
                
                medico = Medico.objects.create(
                    user=auth_user_medico,
                    especialidad=especialidad,
                    matricula=f"MAT-{auth_user_medico.id}",
                    telefono="000-000-0000"
                )
                self.stdout.write(f"✅ Creado registro de Médico para {medico_username}")
            
            # Crear el turno
            fecha_turno = datetime.now() + timedelta(days=7)  # Turno para la próxima semana
            
            with transaction.atomic():
                turno = Turno.objects.create(
                    usuario=auth_user_paciente,  # El usuario que creó el turno
                    paciente=paciente,           # El paciente del turno
                    medico=medico,              # El médico del turno
                    fecha=fecha_turno.date(),
                    hora=fecha_turno.time(),
                    estado="pendiente"
                )
                
                self.stdout.write(f"✅ Turno creado exitosamente!")
                self.stdout.write(f"   ID: {turno.id}")
                self.stdout.write(f"   Usuario: {turno.usuario.username}")
                self.stdout.write(f"   Paciente: {turno.paciente.user.username} (ID: {turno.paciente.id})")
                self.stdout.write(f"   Médico: {turno.medico.user.username} (ID: {turno.medico.id})")
                self.stdout.write(f"   Fecha: {turno.fecha}")
                self.stdout.write(f"   Hora: {turno.hora}")
                
                # Verificar que se puede leer el turno
                turno_verificacion = Turno.objects.get(id=turno.id)
                self.stdout.write(f"✅ Verificación: Turno {turno_verificacion.id} existe en la base de datos")
                
        except AuthUser.DoesNotExist as e:
            self.stdout.write(f"❌ Error: Usuario no encontrado - {e}")
        except Persona.DoesNotExist as e:
            self.stdout.write(f"❌ Error: Persona no encontrada - {e}")
        except Exception as e:
            self.stdout.write(f"❌ Error inesperado: {e}")
            import traceback
            self.stdout.write(traceback.format_exc())
