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
