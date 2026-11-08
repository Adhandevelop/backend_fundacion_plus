from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.accounts.models import Role
from apps.audit.models import AuditAccess, AuditPermission


class AuthAndRBACTests(APITestCase):
    """Pruebas de autenticación JWT/Token, registro ciudadano, RBAC y auditoría inmutable sobre las tablas de plus."""

    def setUp(self):
        user_model = get_user_model()
        self.cliente = user_model.objects.create_user(
            username='cliente1',
            email='cliente1@plus.org',
            password='ClaveSegura123!',
            nombres='Carlos',
            apellidos='Ciudadano',
        )
        self.admin = user_model.objects.create_user(
            username='admin1',
            email='admin1@plus.org',
            password='ClaveAdmin123!',
            nombres='Ana',
            apellidos='Administradora',
            is_staff=True,
        )

    def test_legacy_and_jwt_login_returns_tokens_and_logs_access(self):
        response = self.client.post(
            '/api/login/',
            {'username': 'cliente1', 'password': 'ClaveSegura123!'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['usuario'], 'cliente1')
        self.assertEqual(response.data['rol'], 'cliente')
        self.assertEqual(response.data['primary_role'], Role.Nombre.CIUDADANO)
        self.assertEqual(AuditAccess.objects.filter(resultado='exitoso').count(), 1)

    def test_citizen_registration_requires_data_policy_consent(self):
        bad_resp = self.client.post(
            '/api/v1/auth/register/',
            {
                'correo': 'nuevo@plus.org',
                'password': 'PasswordSeguro2026!',
                'nombres': 'Laura',
                'apellidos': 'Gómez',
                'accepts_data_policy': False,
            },
            format='json',
        )
        self.assertEqual(bad_resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(bad_resp.data['code'], 'validation_error')

        ok_resp = self.client.post(
            '/api/v1/auth/register/',
            {
                'correo': 'nuevo@plus.org',
                'password': 'PasswordSeguro2026!',
                'nombres': 'Laura',
                'apellidos': 'Gómez',
                'accepts_data_policy': True,
            },
            format='json',
        )
        self.assertEqual(ok_resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', ok_resp.data)
        self.assertEqual(ok_resp.data['user']['primary_role'], Role.Nombre.CIUDADANO)

    def test_role_endpoints_enforce_authorization(self):
        cliente_token = Token.objects.create(user=self.cliente)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {cliente_token.key}')

        admin_users_resp = self.client.get('/api/v1/admin/users/')
        self.assertEqual(admin_users_resp.status_code, status.HTTP_403_FORBIDDEN)

        legacy_admin_resp = self.client.get('/api/administrativos/me/')
        self.assertEqual(legacy_admin_resp.status_code, status.HTTP_403_FORBIDDEN)

        admin_token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        ok_admin_resp = self.client.get('/api/v1/admin/users/')
        self.assertEqual(ok_admin_resp.status_code, status.HTTP_200_OK)

    def test_role_change_records_auditoria_permisos(self):
        admin_token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')

        ok_resp = self.client.post(
            f'/api/v1/admin/users/{self.cliente.id}/roles/',
            {'role_code': 'representante', 'motivo': 'Designación territorial'},
            format='json',
        )
        self.assertEqual(ok_resp.status_code, status.HTTP_200_OK)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.get_primary_role(), Role.Nombre.REPRESENTANTE)
        self.assertEqual(AuditPermission.objects.filter(usuario_afectado=self.cliente).count(), 1)

    def test_audit_tables_are_immutable(self):
        self.client.post(
            '/api/v1/auth/login/',
            {'correo': 'cliente1@plus.org', 'password': 'ClaveSegura123!'},
            format='json',
        )
        access_entry = AuditAccess.objects.first()
        self.assertIsNotNone(access_entry)
        access_entry.resultado = 'fallido'
        with self.assertRaises(PermissionDenied):
            access_entry.save()
        with self.assertRaises(PermissionDenied):
            access_entry.delete()
