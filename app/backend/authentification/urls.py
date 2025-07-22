from django.urls import path
from . import views

urlpatterns = [
    # URLs para interfaz web
    path('login/', views.login_form, name='login'),
    path('process_login/', views.process_login, name='process_login'),
    path('register/', views.register_form, name='register'),
    path('process_register/', views.process_register, name='process_register'),
    path('logout/', views.logout_view, name='logout'),
    # Note: API URLs are now defined in main urls.py to avoid conflicts
]
