from django import forms
from .models import AuthUser, Persona

class AuthUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = AuthUser
        fields = ['username', 'password']

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'tipo_usuario',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'direccion',
            'telefono',
            'especialidad',
            'consultorio'
        ]
        