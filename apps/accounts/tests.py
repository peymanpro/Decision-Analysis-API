from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class RegistrationTests(APITestCase):
    def test_registers_user(self):
        response = self.client.post("/api/v1/auth/register/", {
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "StrongPass123!",
        }, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(
            username="existing_user",
            email="existing@example.com",
            password="StrongPass123!",
        )

        response = self.client.post("/api/v1/auth/register/", {
            "username": "existing_user",
            "email": "another@example.com",
            "password": "StrongPass123!",
        }, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            username="first_user",
            email="existing@example.com",
            password="StrongPass123!",
        )

        response = self.client.post("/api/v1/auth/register/", {
            "username": "second_user",
            "email": "EXISTING@example.com",
            "password": "StrongPass123!",
        }, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username="jwt_user",
            password="StrongPass123!",
        )

    def test_obtain_token_pair(self):
        response = self.client.post("/api/v1/auth/token/", {
            "username": "jwt_user",
            "password": "StrongPass123!",
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials_are_rejected(self):
        response = self.client.post("/api/v1/auth/token/", {
            "username": "jwt_user",
            "password": "WrongPassword!"
        }, format="json")

        self.assertEqual(response.status_code, 401)
