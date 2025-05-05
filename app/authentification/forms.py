from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Pacient

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['especialidad', 'consultorio']

class PacientRegisterForm(forms.ModelForm):
    class Meta:
        model = Pacient
        fields = ['fecha_nacimiento', 'direccion', 'telefono']