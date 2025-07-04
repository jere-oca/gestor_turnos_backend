import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthAPITest(TestCase):
    def setUp(self):
        # Crea un usuario para login y cambio de contraseña
        self.username = "20345678"
        self.password = "Clave1234"
        self.email = "test@ejemplo.com"
        self.first_name = "Test"
        self.last_name = "User"
        self.rol = "secretario"

        
    def execute_post_request(self, url, data_dict):
        return self.client.post(
            url,
            json.dumps(data_dict),
            content_type="application/json"
        )


    def test_register(self):
        register_data = {
            "username": self.username,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "rol": self.rol
        }
        
        response = self.execute_post_request(reverse("api_register"), register_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=self.username).exists())


    def test_login(self):
        login_data = {
            "username": self.username,
            "password": self.password
        }
        response = self.execute_post_request(reverse("api_login"), login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("sessionid", response.cookies) # Cookie
    

    def test_password_change(self):
        self.client.login(username=self.username, password=self.password)
        newdata = {
            "old_password": self.password,
            "new_password": "ClaveNueva123"
        }
        response = self.execute_post_request(reverse("api_password_change"), newdata)
        self.assertEqual(response.status_code, 200)
        # Verifica que la contraseña fue cambiada
        user = User.objects.get(username=self.username)
        self.assertTrue(user.check_password("ClaveNueva123"))

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse("api_logout"))
        self.assertEqual(response.status_code, 200)
        # Verifica que la cookie de sesión fue eliminada
        self.assertNotIn("sessionid", self.client.cookies)
        