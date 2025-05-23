import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from authentification.models import AuthUser, Persona
from faker import Faker # Changed from datagen_utils
import random
import datetime

class Command(BaseCommand):
    help = 'Genera usuarios falsos y los exporta a archivos CSV'

    def add_arguments(self, parser):
        parser.add_argument('--cantidad', type=int, default=1000,
                            help='Cantidad de usuarios a generar (default: 1000)')
        parser.add_argument('--output', type=str, default='csv_export',
                            help='Carpeta donde se guardarán los archivos CSV (default: csv_export)')

    def handle(self, *args, **kwargs):
        cantidad = kwargs['cantidad']
        output_dir = kwargs['output']
        
        # Crear directorio si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        fake = Faker('es_ES')
        
        # Tipos de usuario disponibles
        tipos_usuario = ['doctor', 'paciente', 'administrativo']
        
        # Especialidades médicas para doctores
        especialidades = [
            'Cardiología', 'Dermatología', 'Endocrinología', 
            'Gastroenterología', 'Ginecología', 'Neurología',
            'Oftalmología', 'Oncología', 'Pediatría',
            'Psiquiatría', 'Traumatología', 'Urología'
        ]
        
        # Consultorios para doctores
        consultorios = [f'Consultorio {i}' for i in range(1, 11)]
        
        self.stdout.write(f'Generando {cantidad} usuarios falsos para exportación...')
        
        # Archivos CSV para AuthUser y Persona
        auth_users_file = os.path.join(output_dir, 'auth_users.csv')
        personas_file = os.path.join(output_dir, 'personas.csv')
        
        # Generar usuarios y exportar a CSV
        with open(auth_users_file, 'w', newline='', encoding='utf-8') as auth_file, \
             open(personas_file, 'w', newline='', encoding='utf-8') as pers_file:
            
            auth_writer = csv.writer(auth_file)
            auth_writer.writerow(['id', 'username', 'password'])
            
            pers_writer = csv.writer(pers_file)
            pers_writer.writerow(['auth_user_id', 'tipo_usuario', 'nombre', 'apellido', 
                                  'fecha_nacimiento', 'direccion', 'telefono', 
                                  'especialidad', 'consultorio'])
            
            for i in range(1, cantidad + 1):
                username = fake.unique.user_name()
                password = make_password(fake.password(length=12))
                
                # Escribir AuthUser
                auth_writer.writerow([i, username, password])
                
                # Datos para Persona
                tipo_usuario = random.choice(tipos_usuario)
                if tipo_usuario == 'doctor':
                    especialidad = random.choice(especialidades)
                    consultorio = random.choice(consultorios)
                else:
                    especialidad = ''
                    consultorio = ''
                
                fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=80)
                
                # Escribir Persona
                pers_writer.writerow([
                    i,  # auth_user_id (clave foránea)
                    tipo_usuario,
                    fake.first_name(),
                    fake.last_name(),
                    fecha_nacimiento,
                    fake.address().replace('\n', ', '),
                    fake.phone_number(),
                    especialidad,
                    consultorio
                ])
                
                if i % 1000 == 0:
                    self.stdout.write(f'Generados {i} registros...')
        
        self.stdout.write(self.style.SUCCESS(
            f'¡{cantidad} usuarios generados y exportados a {auth_users_file} y {personas_file}!'
        ))
