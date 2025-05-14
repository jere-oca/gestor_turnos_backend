from django.urls import path
from .views import login_render
from . import views
urlpatterns = [
    path('login/', login_render, name='login'),
    path('register/', views.persona_register, name='register'),
    
] 
