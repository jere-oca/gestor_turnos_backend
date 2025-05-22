from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Turno

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('usuario__username', 'usuario__email', 'estado')
