from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/csrf/', views.get_csrf, name='get_csrf'),
    path('api/user/', views.api_get_session, name='api_get_session'),
    
]
