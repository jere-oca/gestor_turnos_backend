from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import AuthUser, Persona

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class AuthUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AuthUser
        fields = ('username',)

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
