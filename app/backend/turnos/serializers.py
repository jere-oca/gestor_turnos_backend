from rest_framework import serializers
from .models import Turno, Especialidad, Medico, Paciente

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id', 'nombre']

class MedicoSerializer(serializers.ModelSerializer):
    especialidad = EspecialidadSerializer(read_only=True)
    nombre = serializers.CharField(source='user.persona.nombre', read_only=True)
    apellido = serializers.CharField(source='user.persona.apellido', read_only=True)
    
    class Meta:
        model = Medico
        fields = ['id', 'nombre', 'apellido', 'especialidad', 'matricula']

class PacienteSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='user.persona.nombre', read_only=True)
    apellido = serializers.CharField(source='user.persona.apellido', read_only=True)
    
    class Meta:
        model = Paciente
        fields = ['id', 'nombre', 'apellido', 'dni']

class TurnoSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(read_only=True)
    paciente = PacienteSerializer(read_only=True)
    
    # Campos para escribir IDs
    medico_id = serializers.IntegerField(write_only=True, required=False)
    paciente_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Turno
        fields = ['id', 'fecha', 'hora', 'medico', 'paciente', 'estado', 'medico_id', 'paciente_id']
        read_only_fields = ['estado'] 