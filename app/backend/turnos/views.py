from django.shortcuts import render, redirect, get_object_or_404
from .forms import TurnoForm
from .models import Turno, Especialidad, Medico, Paciente
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    TurnoSerializer, EspecialidadSerializer,
    MedicoSerializer, PacienteSerializer
)

@login_required
def crear_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.usuario = request.user
            turno.save()
            return redirect('listar_turnos')
    else:
        form = TurnoForm()
    return render(request, 'turnos/crear_turno.html', {'form': form})

@login_required
def listar_turnos(request):
    turnos = Turno.objects.filter(usuario=request.user)
    return render(request, 'turnos/listar_turnos.html', {'turnos': turnos})

# Eliminar turno
@login_required
def eliminar_turno(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id, usuario=request.user)
    if request.method == 'POST':
        turno.delete()
        return redirect('listar_turnos')
    return render(request, 'turnos/eliminar_turno.html', {'turno': turno})

# Modificar turno
@login_required
def modificar_turno(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id, usuario=request.user)
    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')
    else:
        form = TurnoForm(instance=turno)
    return render(request, 'turnos/modificar_turno.html', {'form': form, 'turno': turno})

class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Medicos').exists():
            return Turno.objects.filter(medico__user=user)
        elif user.groups.filter(name='Pacientes').exists():
            return Turno.objects.filter(paciente__user=user)
        return Turno.objects.all()

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        turno = self.get_object()
        turno.estado = 'cancelado'
        turno.save()
        return Response({'status': 'turno cancelado'})

class EspecialidadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        especialidad_id = self.request.query_params.get('especialidad', None)
        if especialidad_id:
            return Medico.objects.filter(especialidad_id=especialidad_id)
        return Medico.objects.all()

class PacienteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Pacientes').exists():
            return Paciente.objects.filter(user=user)
        return Paciente.objects.all()