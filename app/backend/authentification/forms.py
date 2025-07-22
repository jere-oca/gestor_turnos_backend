from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import AuthUser, Persona
import hashlib
import base64

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    def verify_password(self, plain_password, hashed_password):
        """
        Verifica si una contraseña en texto plano coincide con un hash de Django
        """
        try:
            algorithm, iterations, salt, hash_value = hashed_password.split('$')
            
            if algorithm != 'pbkdf2_sha256':
                return False
            
            # Generar el hash con los mismos parámetros
            key = hashlib.pbkdf2_hmac(
                'sha256',
                plain_password.encode('utf-8'),
                salt.encode('utf-8'),
                int(iterations)
            )
            
            # Codificar en base64
            generated_hash = base64.b64encode(key).decode('ascii')
            
            return generated_hash == hash_value
        except (ValueError, TypeError):
            # Si el formato no es correcto, intentar comparación directa (para compatibilidad)
            return plain_password == hashed_password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                auth_user = AuthUser.objects.get(username=username)
                # Verificar la contraseña usando hashing
                if self.verify_password(password, auth_user.password):
                    self.user = auth_user
                else:
                    raise forms.ValidationError('Usuario o contraseña incorrectos.')
            except AuthUser.DoesNotExist:
                raise forms.ValidationError('Usuario o contraseña incorrectos.')
        return cleaned_data

    def get_user(self):
        return self.user if hasattr(self, 'user') else None

class AuthUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    def make_password(self, raw_password):
        """
        Genera un hash PBKDF2 para la contraseña
        """
        import os
        
        # Generar un salt aleatorio
        salt = base64.b64encode(os.urandom(12)).decode('ascii')
        iterations = 1000000
        
        # Generar el hash
        key = hashlib.pbkdf2_hmac(
            'sha256',
            raw_password.encode('utf-8'),
            salt.encode('utf-8'),
            iterations
        )
        
        # Codificar en base64
        hash_value = base64.b64encode(key).decode('ascii')
        
        return f'pbkdf2_sha256${iterations}${salt}${hash_value}'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Hashear la contraseña antes de guardar
        user.password = self.make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
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
        