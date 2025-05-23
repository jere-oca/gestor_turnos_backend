from django.db import models

# Create your models here.
# turnos/models.py

from django.db import models
from django.contrib.auth.models import User

class Turno(models.Model):
    fecha = models.DateField()  # La fecha del turno
    hora = models.TimeField()  # La hora del turno
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User
    estado = models.CharField(max_length=20, default='pendiente')  # Estado del turno (pendiente, confirmado, etc.)
    
    def __str__(self):
        return f"Turno {self.id} para {self.usuario} el {self.fecha} a las {self.hora}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=10, unique=True, db_index=True)
    celular = models.CharField(max_length=20)
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"
