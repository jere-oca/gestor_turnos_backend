from django.db import models
from django.contrib.auth.models import User

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.especialidad}"

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()

    def __str__(self):
        return f"{self.user.get_full_name()} - DNI: {self.dni}"

class Turno(models.Model):
    fecha = models.DateField()  # La fecha del turno
    hora = models.TimeField()  # La hora del turno
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=20, default='pendiente')  # Estado del turno (pendiente, confirmado, etc.)
    
    def __str__(self):
        if self.medico and self.paciente:
            return f"Turno {self.id} para {self.paciente} con Dr. {self.medico} el {self.fecha} a las {self.hora}"
        return f"Turno {self.id} para {self.usuario} el {self.fecha} a las {self.hora}"
