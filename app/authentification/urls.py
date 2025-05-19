from django.urls import path
from . import views

urlpatterns = [
    # URLs para la interfaz web
    path('login/', views.login_form, name='login'),
    path('login/process/', views.process_login, name='login-process'),
    path('register/', views.register_form, name='register'),
    path('register/process/', views.process_register, name='register-process'),
    path('logout/', views.logout_view, name='logout'),
    # URLs para la API
    path('api/auth/login/', views.api_login, name='api-login'),
] 
