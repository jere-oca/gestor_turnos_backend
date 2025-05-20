from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import AuthUser, Persona

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                self.user = AuthUser.objects.get(username=username, password=password)
            except AuthUser.DoesNotExist:
                raise forms.ValidationError('Usuario o contraseña incorrectos.')
        return cleaned_data

    def get_user(self):
        return self.user if hasattr(self, 'user') else None

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
        