from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthAPITest(TestCase):
    def setUp(self):
        # Crea un usuario para login y cambio de contraseña
        self.username = "12345678"
        self.password = "Clave1234"
        self.email = "test@ejemplo.com"
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)

    def test_register(self):
        data = {
            "username": "87654321",
            "password": "OtraClave123",
            "email": "nuevo@ejemplo.com"
        }
        response = self.client.post(reverse("api_register"), data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="87654321").exists())

    def test_login_and_cookie(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(reverse("api_login"), data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("sessionid", response.cookies) # Verifica la cookie de sesión
    

    def test_password_change(self):
        self.client.login(username=self.username, password=self.password)
        data = {
            "old_password": self.password,
            "new_password": "ClaveNueva123"
        }
        response = self.client.post(reverse("api_password_change"), data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # Verifica que la contraseña fue cambiada
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("ClaveNueva123"))
