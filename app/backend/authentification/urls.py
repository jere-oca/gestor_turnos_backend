from django.urls import path
from . import views

urlpatterns = [

    # Endpoints web (formulario)
    path('login/', views.login_form, name='login_form'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_form, name='register_form'),
    path('login/submit/', views.process_login, name='process_login'),
    path('register/submit/', views.process_register, name='process_register'),

    # Endpoints API
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/csrf/', views.get_csrf, name='get_csrf'),
    path('api/user/', views.api_get_session, name='api_get_session'),
    # Endpoint temporal para debug de Redis
    path('api/debug/redis/', views.debug_redis_key, name='debug_redis_key'),
    path('api/redis/keys/', views.redis_keys_view, name='redis_keys_view'),
    # URLs para interfaz web
    path('login/', views.login_form, name='login'),
    path('process_login/', views.process_login, name='process_login'),
    path('register/', views.register_form, name='register'),
    path('process_register/', views.process_register, name='process_register'),
    path('logout/', views.logout_view, name='logout'),
    # Note: API URLs are now defined in main urls.py to avoid conflicts

]
