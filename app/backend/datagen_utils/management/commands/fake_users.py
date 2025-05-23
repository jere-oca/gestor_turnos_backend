from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from ...models import User
from datagen_utils import Faker
import random

class Command(BaseCommand):
    help = 'Genera usuarios falsos'

    def handle(self, *args, **kwargs):
        fake = Faker('es_AR')
        batch_size = 10
        total = 300000
        users = []
        roles = [choice[1] for choice in User.ROLE_CHOICES]
        for i in range(total):
            name = fake.first_name()
            surname = fake.last_name()
            email = fake.unique.email()
            role = random.choice(roles)
            password = make_password(fake.password(length=10))
            users.append(User(
                name=name,
                surname=surname,
                email=email,
                password=password,
                role = role
            ))
            if len(users) >= batch_size:
                User.objects.bulk_create(users)
                users = []
                self.stdout.write(f'{i+1} usuarios insertados...')
        if users:
            User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS(f'¡{total} usuarios creados!'))