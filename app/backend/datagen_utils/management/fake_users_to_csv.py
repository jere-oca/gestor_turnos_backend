import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from ...models import User
from datagen_utils import Faker
import random

class Command(BaseCommand):
    help = 'Genera usuarios falsos y los exporta a un archivo CSV'

    def handle(self, *args, **kwargs):
        fake = Faker('es_AR')
        total = 300000
        roles = [choice[1] for choice in User.ROLE_CHOICES]
        csv_file = 'fake_users.csv'

        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'surname', 'email', 'password', 'role'])  # Encabezados del CSV

            for i in range(total):
                name = fake.first_name()
                surname = fake.last_name()
                email = fake.unique.email()
                role = random.choice(roles)
                password = make_password(fake.password(length=10))
                writer.writerow([name, surname, email, password, role])

                if (i + 1) % 100 == 0:
                    self.stdout.write(f'{i+1} usuarios generados...')

        self.stdout.write(self.style.SUCCESS(f'¡{total} usuarios exportados a {csv_file}!'))