from django.core.management.base import BaseCommand
from authentification.models import AuthUser, Persona
from django.db import connection, reset_queries
import time
import random
from django.db.models import Q

class Command(BaseCommand):
    help = 'Realiza pruebas de rendimiento en consultas con y sin índices'

    def add_arguments(self, parser):
        parser.add_argument('--queries', type=int, default=100,
                            help='Número de consultas a ejecutar (default: 100)')
        
    def time_query(self, query_func, iterations):
        """Mide el tiempo para ejecutar una consulta varias veces"""
        reset_queries()
        start_time = time.time()
        
        for _ in range(iterations):
            query_func()
            
        end_time = time.time()
        return end_time - start_time, len(connection.queries)

    def handle(self, *args, **kwargs):
        iterations = kwargs['queries']
        self.stdout.write(f"Ejecutando {iterations} consultas para cada prueba...")
        
        # 1. Consulta por username (ya tiene índice por defecto)
        def query_by_username():
            # Obtener un nombre de usuario aleatorio existente
            user_count = AuthUser.objects.count()
            if user_count > 0:
                random_id = random.randint(1, user_count)
                user = AuthUser.objects.filter(id=random_id).first()
                if user:
                    AuthUser.objects.filter(username=user.username).exists()
        
        time_username, queries_username = self.time_query(query_by_username, iterations)
        self.stdout.write(f"Tiempo para consultar por username: {time_username:.4f} segundos")
        self.stdout.write(f"Número de consultas: {queries_username}")
        
        # 2. Consulta por tipo_usuario
        def query_by_tipo_usuario():
            tipos = ['doctor', 'paciente', 'administrativo']
            random_tipo = random.choice(tipos)
            Persona.objects.filter(tipo_usuario=random_tipo).count()
        
        time_tipo, queries_tipo = self.time_query(query_by_tipo_usuario, iterations)
        self.stdout.write(f"Tiempo para consultar por tipo_usuario: {time_tipo:.4f} segundos")
        self.stdout.write(f"Número de consultas: {queries_tipo}")
        
        # 3. Búsqueda por nombre o apellido (consulta más compleja)
        def query_by_name_or_surname():
            # Obtener una persona aleatoria
            persona_count = Persona.objects.count()
            if persona_count > 0:
                random_id = random.randint(1, persona_count)
                persona = Persona.objects.filter(auth_user_id=random_id).first()
                if persona:
                    term = persona.nombre[:3]  # Primeras 3 letras del nombre
                    Persona.objects.filter(
                        Q(nombre__startswith=term) | 
                        Q(apellido__startswith=term)
                    ).count()
        
        time_name, queries_name = self.time_query(query_by_name_or_surname, iterations)
        self.stdout.write(f"Tiempo para consulta por nombre/apellido: {time_name:.4f} segundos")
        self.stdout.write(f"Número de consultas: {queries_name}")
        
        # Resumen
        self.stdout.write(self.style.SUCCESS(f"\nResumen de tiempos para {iterations} consultas:"))
        self.stdout.write(f"Consulta por username: {time_username:.4f} s")
        self.stdout.write(f"Consulta por tipo_usuario: {time_tipo:.4f} s")
        self.stdout.write(f"Consulta por nombre/apellido: {time_name:.4f} s")
        
        # Sugerencias de índice basadas en rendimiento
        if time_tipo > time_username * 1.5:
            self.stdout.write(self.style.WARNING(
                "\nSugerencia: Crear índice en 'Persona.tipo_usuario' podría mejorar el rendimiento."
            ))
            self.stdout.write("Para crear este índice, añada la siguiente migración:")
            self.stdout.write("""
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('authentification', 'XXXX_last_migration'),  # Reemplazar con la última migración
    ]

    operations = [
        migrations.AddIndex(
            model_name='persona',
            index=models.Index(fields=['tipo_usuario'], name='persona_tipo_idx'),
        ),
    ]
            """)
            
        if time_name > time_username * 2:
            self.stdout.write(self.style.WARNING(
                "\nSugerencia: Crear índices en 'Persona.nombre' y 'Persona.apellido' podría mejorar el rendimiento."
            ))
            self.stdout.write("Para crear estos índices, añada la siguiente migración:")
            self.stdout.write("""
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('authentification', 'XXXX_last_migration'),  # Reemplazar con la última migración
    ]

    operations = [
        migrations.AddIndex(
            model_name='persona',
            index=models.Index(fields=['nombre'], name='persona_nombre_idx'),
        ),
        migrations.AddIndex(
            model_name='persona',
            index=models.Index(fields=['apellido'], name='persona_apellido_idx'),
        ),
    ]
            """)
