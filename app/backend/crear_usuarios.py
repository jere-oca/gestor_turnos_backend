#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_turnos.settings')
django.setup()

from authentification.models import AuthUser, Persona
from turnos.models import Especialidad, Medico, Paciente
from django.db import transaction

def crear_usuarios():
    print("🔄 Creando usuarios de prueba...")
    
    try:
        with transaction.atomic():
            # Crear especialidad si no existe
            especialidad, created = Especialidad.objects.get_or_create(
                nombre="Medicina General",
                defaults={'descripcion': "Especialidad general"}
            )
            if created:
                print(f"✅ Especialidad creada: {especialidad.nombre}")
            
            # Crear usuario melisahernandez
            auth_user, created = AuthUser.objects.get_or_create(
                username='melisahernandez',
                defaults={
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False
                }
            )
            
            if created:
                auth_user.set_password('T_0SDlq9)n0N')
                auth_user.save()
                print(f"✅ Usuario creado: {auth_user.username}")
            else:
                print(f"ℹ️  Usuario ya existe: {auth_user.username}")
            
            # Crear Persona
            persona, created = Persona.objects.get_or_create(
                auth_user=auth_user,
                defaults={
                    'tipo_usuario': 'paciente',
                    'nombre': 'Melisa',
                    'apellido': 'Hernandez',
                    'email': 'melisahernandez@test.com'
                }
            )
            
            if created:
                print(f"✅ Persona creada: {persona.nombre} ({persona.tipo_usuario})")
            else:
                print(f"ℹ️  Persona ya existe: {persona.nombre} ({persona.tipo_usuario})")
            
            # Crear registro de Paciente
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
                print(f"✅ Paciente creado: {paciente.dni}")
            
            # Crear un doctor para las pruebas
            auth_user_doctor, created = AuthUser.objects.get_or_create(
                username='doctor1',
                defaults={
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False
                }
            )
            
            if created:
                auth_user_doctor.set_password('test123')
                auth_user_doctor.save()
                print(f"✅ Doctor creado: {auth_user_doctor.username}")
            
            # Crear Persona para doctor
            persona_doctor, created = Persona.objects.get_or_create(
                auth_user=auth_user_doctor,
                defaults={
                    'tipo_usuario': 'doctor',
                    'nombre': 'Doctor',
                    'apellido': 'Prueba',
                    'email': 'doctor1@test.com'
                }
            )
            
            # Crear registro de Médico
            medico, created = Medico.objects.get_or_create(
                user=auth_user_doctor,
                defaults={
                    'especialidad': especialidad,
                    'matricula': f"MAT{auth_user_doctor.id:06d}",
                    'telefono': "000-000-0000"
                }
            )
            if created:
                print(f"✅ Médico creado: {medico.matricula}")
            
            print("\n🎉 Usuarios de prueba creados exitosamente!")
            print("\nUsuarios disponibles:")
            print(f"   👤 melisahernandez (paciente) - Password: T_0SDlq9)n0N")
            print(f"   👤 doctor1 (doctor) - Password: test123")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_usuarios()
