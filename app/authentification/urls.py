from django.urls import path
from . import views

urlpatterns = [
    # URLs para la interfaz web
    path('login/', views.login_form, name='login'),
    path('login/process/', views.process_login, name='login-process'),
    path('register/', views.register_form, name='register'),
    path('register/process/', views.process_register, name='register-process'),
    
    # URLs para la API
    path('api/login/', views.api_login, name='api-login'),
] 
