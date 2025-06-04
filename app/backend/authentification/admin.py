from django.contrib import admin
from .models import AuthUser, Persona

@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('username',)

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        'auth_user', 'tipo_usuario', 'nombre', 'apellido',
        'fecha_nacimiento', 'especialidad', 'consultorio'
    )
    search_fields = (
        'nombre', 'apellido', 'tipo_usuario', 'auth_user__username', 'especialidad', 'consultorio'
    )
    list_filter = ('tipo_usuario', 'especialidad', 'consultorio')
