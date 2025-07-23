from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
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
    permission_classes = [permissions.IsAuthenticated]  # Restaurar autenticación

    def perform_create(self, serializer):
        # Obtener el usuario autenticado desde la sesión
        auth_user_id = self.request.session.get('auth_user_id')
        if auth_user_id:
            from authentification.models import AuthUser, Persona
            try:
                auth_user = AuthUser.objects.get(id=auth_user_id)
                persona = Persona.objects.get(auth_user=auth_user)
                
                medico_id = serializer.validated_data.get('medico_id')
                paciente_id = serializer.validated_data.get('paciente_id')
                
                from .models import Medico, Paciente
                medico = None
                paciente = None
                
                # Obtener el médico
                if medico_id:
                    try:
                        medico = Medico.objects.get(id=medico_id)
                    except Medico.DoesNotExist:
                        medico = None
                
                # Lógica para asignar el paciente según el tipo de usuario
                if persona.tipo_usuario == 'paciente':
                    # Si el usuario es paciente, automáticamente asignarlo como el paciente del turno
                    try:
                        paciente = Paciente.objects.get(user=auth_user)
                    except Paciente.DoesNotExist:
                        # Si no existe el registro de Paciente, crearlo
                        paciente = Paciente.objects.create(
                            user=auth_user,
                            dni=f"DNI-{auth_user.id}",  # DNI temporal
                            fecha_nacimiento="1990-01-01",  # Fecha temporal
                            telefono="000-000-0000",  # Teléfono temporal
                            direccion="Dirección pendiente"  # Dirección temporal
                        )
                else:
                    # Si es médico o administrativo, usar el paciente_id proporcionado
                    if paciente_id:
                        try:
                            paciente = Paciente.objects.get(id=paciente_id)
                        except Paciente.DoesNotExist:
                            paciente = None
                
                # Guardar el turno con los objetos encontrados
                serializer.save(usuario=auth_user, medico=medico, paciente=paciente)
                return
            except (AuthUser.DoesNotExist, Persona.DoesNotExist):
                pass
        # Si no hay usuario autenticado, lanzar error
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("Usuario no autenticado")

    def get_object(self):
        """
        Obtiene un turno específico, pero solo si el usuario tiene permisos para verlo
        """
        obj = super().get_object()
        
        # Obtener el usuario autenticado
        auth_user_id = self.request.session.get('auth_user_id')
        if not auth_user_id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Usuario no autenticado")
        
        try:
            from authentification.models import AuthUser, Persona
            auth_user = AuthUser.objects.get(id=auth_user_id)
            persona = Persona.objects.get(auth_user=auth_user)
            
            # Verificar permisos según el tipo de usuario
            if persona.tipo_usuario == 'paciente':
                # Los pacientes solo pueden ver sus propios turnos
                if obj.paciente and obj.paciente.user == auth_user:
                    return obj
                else:
                    from rest_framework.exceptions import PermissionDenied
                    raise PermissionDenied("No tienes permiso para ver este turno")
                    
            elif persona.tipo_usuario == 'doctor':
                # Los médicos solo pueden ver turnos donde ellos son el médico
                if obj.medico and obj.medico.user == auth_user:
                    return obj
                else:
                    from rest_framework.exceptions import PermissionDenied
                    raise PermissionDenied("No tienes permiso para ver este turno")
                    
            elif persona.tipo_usuario == 'administrativo':
                # Los administrativos pueden ver todos los turnos
                return obj
                
            else:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Tipo de usuario no reconocido")
                
        except (AuthUser.DoesNotExist, Persona.DoesNotExist):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Usuario no encontrado")

    def get_queryset(self):
        # Obtener el auth_user_id de la sesión
        auth_user_id = self.request.session.get('auth_user_id')
        if not auth_user_id:
            return Turno.objects.none()  # Sin usuario autenticado, no devolver turnos
        
        try:
            from authentification.models import AuthUser, Persona
            auth_user = AuthUser.objects.get(id=auth_user_id)
            persona = Persona.objects.get(auth_user=auth_user)
            
            # DEBUG: Imprimir información para debugging
            print(f"[DEBUG] Usuario autenticado: {auth_user.username} (ID: {auth_user.id})")
            print(f"[DEBUG] Tipo de usuario: {persona.tipo_usuario}")
            
            # Filtrar según el tipo de usuario
            if persona.tipo_usuario == 'paciente':
                # Los pacientes solo ven turnos donde ELLOS son el paciente asignado
                queryset = Turno.objects.filter(paciente__user=auth_user)
                print(f"[DEBUG] Filtro para paciente: paciente__user={auth_user.id}")
                print(f"[DEBUG] Turnos encontrados: {queryset.count()}")
                for turno in queryset:
                    print(f"[DEBUG] Turno {turno.id}: paciente_id={turno.paciente.id if turno.paciente else None}, paciente_user_id={turno.paciente.user.id if turno.paciente else None}")
                return queryset
                    
            elif persona.tipo_usuario == 'doctor':
                # Los médicos solo ven turnos donde ELLOS son el médico asignado
                queryset = Turno.objects.filter(medico__user=auth_user)
                print(f"[DEBUG] Filtro para doctor: medico__user={auth_user.id}")
                print(f"[DEBUG] Turnos encontrados: {queryset.count()}")
                return queryset
                    
            elif persona.tipo_usuario == 'administrativo':
                # Los administrativos pueden ver todos los turnos
                queryset = Turno.objects.all()
                print(f"[DEBUG] Administrativo: mostrando todos los turnos ({queryset.count()})")
                return queryset
                
            else:
                # Tipo de usuario no reconocido, no mostrar turnos
                print(f"[DEBUG] Tipo de usuario no reconocido: {persona.tipo_usuario}")
                return Turno.objects.none()
                
        except (AuthUser.DoesNotExist, Persona.DoesNotExist):
            print(f"[DEBUG] Error: Usuario o persona no encontrada para auth_user_id={auth_user_id}")
            return Turno.objects.none()

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