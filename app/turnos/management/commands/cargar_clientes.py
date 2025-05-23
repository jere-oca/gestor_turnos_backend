from django.core.management.base import BaseCommand
from turnos.models import Cliente
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Carga 500,000 clientes de prueba'

    def handle(self, *args, **kwargs):
        fake = Faker('es_AR')
        clientes = []
        for i in range(500_000):
            nombre = fake.first_name()
            apellido = fake.last_name()
            dni = str(20_000_000 + i)  # DNI único
            celular = fake.phone_number()
            email = f"{nombre.lower()}.{apellido.lower()}{i}@mail.com"
            clientes.append(Cliente(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                celular=celular,
                email=email
            ))
            if len(clientes) >= 5000:
                Cliente.objects.bulk_create(clientes)
                clientes = []
                self.stdout.write(f"{i+1} clientes cargados...")
        if clientes:
            Cliente.objects.bulk_create(clientes)
        self.stdout.write(self.style.SUCCESS('Carga completa de 500,000 clientes.'))