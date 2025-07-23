from django.core.management.base import BaseCommand
from django.db import transaction
from authentification.models import AuthUser, Persona
from turnos.models import Turno, Paciente, Medico

class Command(BaseCommand):
    help = 'Verifica y corrige la asociación de turnos con pacientes'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Verificando asociaciones de turnos...")
        
        # Verificar todos los turnos
        turnos = Turno.objects.all()
        self.stdout.write(f"📊 Total de turnos encontrados: {turnos.count()}")
        
        turnos_sin_paciente = 0
        turnos_corregidos = 0
        
        for turno in turnos:
            self.stdout.write(f"\n🔸 Turno {turno.id}:")
            self.stdout.write(f"   Usuario: {turno.usuario.username} (ID: {turno.usuario.id})")
            self.stdout.write(f"   Paciente: {turno.paciente.user.username if turno.paciente else 'None'} (ID: {turno.paciente.id if turno.paciente else 'None'})")
            self.stdout.write(f"   Médico: {turno.medico.user.username if turno.medico else 'None'} (ID: {turno.medico.id if turno.medico else 'None'})")
            
            # Verificar si el usuario es paciente pero no está asignado como paciente del turno
            try:
                persona = Persona.objects.get(auth_user=turno.usuario)
                if persona.tipo_usuario == 'paciente':
                    try:
                        paciente = Paciente.objects.get(user=turno.usuario)
                        if turno.paciente != paciente:
                            self.stdout.write(f"   ⚠️  PROBLEMA: Usuario es paciente pero turno no está asociado correctamente")
                            self.stdout.write(f"      Esperado: Paciente ID {paciente.id}")
                            self.stdout.write(f"      Actual: Paciente ID {turno.paciente.id if turno.paciente else 'None'}")
                            
                            # Corregir la asociación
                            with transaction.atomic():
                                turno.paciente = paciente
                                turno.save()
                                turnos_corregidos += 1
                                self.stdout.write(f"   ✅ CORREGIDO: Turno asociado al paciente correcto")
                        else:
                            self.stdout.write(f"   ✅ OK: Turno correctamente asociado")
                    except Paciente.DoesNotExist:
                        self.stdout.write(f"   ⚠️  PROBLEMA: Usuario es paciente pero no tiene registro en tabla Paciente")
                        turnos_sin_paciente += 1
                else:
                    self.stdout.write(f"   ℹ️  Usuario tipo: {persona.tipo_usuario}")
            except Persona.DoesNotExist:
                self.stdout.write(f"   ❌ ERROR: Usuario no tiene registro en tabla Persona")
        
        self.stdout.write(f"\n📈 Resumen:")
        self.stdout.write(f"   Turnos corregidos: {turnos_corregidos}")
        self.stdout.write(f"   Turnos sin paciente válido: {turnos_sin_paciente}")
        
        # Mostrar estadísticas de usuarios
        self.stdout.write(f"\n👥 Estadísticas de usuarios:")
        for persona in Persona.objects.all():
            auth_user = persona.auth_user
            turnos_como_usuario = Turno.objects.filter(usuario=auth_user).count()
            turnos_como_paciente = Turno.objects.filter(paciente__user=auth_user).count()
            turnos_como_medico = Turno.objects.filter(medico__user=auth_user).count()
            
            self.stdout.write(f"   {auth_user.username} ({persona.tipo_usuario}):")
            self.stdout.write(f"     - Turnos como usuario: {turnos_como_usuario}")
            self.stdout.write(f"     - Turnos como paciente: {turnos_como_paciente}")
            self.stdout.write(f"     - Turnos como médico: {turnos_como_medico}")
