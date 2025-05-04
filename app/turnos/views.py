from django.shortcuts import render, redirect
from .forms import TurnoForm
from .models import Turno
from django.contrib.auth.decorators import login_required

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
