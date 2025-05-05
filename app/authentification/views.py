import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Doctor, Pacient
from .forms import UserRegisterForm, DoctorRegisterForm, PacientRegisterForm
from django.db import transaction

@csrf_exempt
def doctor_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_form = UserRegisterForm(data)
            doctor_form = DoctorRegisterForm(data)
            if user_form.is_valid() and doctor_form.is_valid():
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.save()
                    doctor = doctor_form.save(commit=False)
                    doctor.user = user
                    doctor.save()
                return JsonResponse({'success': True, 'message': 'Doctor registrado correctamente.'}, status=201)
            else:
                errors = {**user_form.errors, **doctor_form.errors}
                return JsonResponse({'success': False, 'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def pacient_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_form = UserRegisterForm(data)
            paciente_form = PacientRegisterForm(data)
            if user_form.is_valid() and paciente_form.is_valid():
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.save()
                    paciente = paciente_form.save(commit=False)
                    paciente.user = user
                    paciente.save()
                return JsonResponse({'success': True, 'message': 'Paciente registrado correctamente.'}, status=201)
            else:
                errors = {**user_form.errors, **paciente_form.errors}
                return JsonResponse({'success': False, 'errors': errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)