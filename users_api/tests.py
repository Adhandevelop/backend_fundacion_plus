from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AuthAndRoleEndpointsTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.cliente = user_model.objects.create_user(
            username='cliente1',
            password='clave-segura-123',
        )
        self.admin = user_model.objects.create_user(
            username='admin1',
            password='clave-admin-123',
            is_staff=True,
        )

    def test_login_with_username_and_password_returns_token_and_role(self):
        response = self.client.post(
            '/api/login/',
            {
                'username': 'cliente1',
                'password': 'clave-segura-123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['usuario'], 'cliente1')
        self.assertEqual(response.data['rol'], 'cliente')

    def test_cliente_endpoint_denies_administrativo_user(self):
        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get('/api/clientes/me/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_administrativo_endpoint_denies_cliente_user(self):
        token = Token.objects.create(user=self.cliente)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get('/api/administrativos/me/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_role_endpoints_accept_matching_user_type(self):
        cliente_token = Token.objects.create(user=self.cliente)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {cliente_token.key}')
        cliente_response = self.client.get('/api/clientes/me/')
        self.assertEqual(cliente_response.status_code, status.HTTP_200_OK)
        self.assertEqual(cliente_response.data['rol'], 'cliente')

        admin_token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        admin_response = self.client.get('/api/administrativos/me/')
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_response.data['rol'], 'administrativo')

# Create your tests here.
