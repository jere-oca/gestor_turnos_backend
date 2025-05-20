from rest_framework import serializers
from .models import Turno, Especialidad, Medico, Paciente

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id', 'nombre']

class MedicoSerializer(serializers.ModelSerializer):
    especialidad = EspecialidadSerializer(read_only=True)
    
    class Meta:
        model = Medico
        fields = ['id', 'nombre', 'apellido', 'especialidad']

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'nombre', 'apellido', 'dni']

class TurnoSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(read_only=True)
    paciente = PacienteSerializer(read_only=True)
    
    class Meta:
        model = Turno
        fields = ['id', 'fecha', 'hora', 'medico', 'paciente', 'estado']
        read_only_fields = ['estado'] 