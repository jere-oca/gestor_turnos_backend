from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class AuthUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, null=False)
    password = models.CharField(max_length=128) 
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='auth_user_set',  # Cambiar el nombre del reverse accessor
        related_query_name='auth_user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='auth_user_set',  # Cambiar el nombre del reverse accessor
        related_query_name='auth_user',
    )


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