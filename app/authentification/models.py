from django.db import models

class AuthUser(models.Model):
    username = models.CharField(max_length=150, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)  # Guarda el hash, no texto plano

    def __str__(self):
        return self.username

class Persona(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('doctor', 'Doctor'),
        ('paciente', 'Paciente'),
        ('administrativo', 'Administrativo'),
    ]
    auth_user = models.OneToOneField(
        AuthUser,
        on_delete=models.CASCADE,
        primary_key=True,  # Esto hace que sea PK y FK a la vez
    )
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, null=False)
    nombre = models.CharField(max_length=100, null=False)
    apellido = models.CharField(max_length=100, null=False)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    consultorio = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo_usuario})"