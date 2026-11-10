import re
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.test import override_settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User
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

    @override_settings(
        FRONTEND_URL='https://fundacionplus.site',
        DEFAULT_FROM_EMAIL='PLUS <notificaciones@fundacionplus.site>',
        PASSWORD_RESET_TIMEOUT=3600,
        PASSWORD_RESET_COOLDOWN_SECONDS=60,
    )
    def test_password_reset_full_flow_resend_email_expiry_and_session_revocation(self):
        cache.clear()
        mail.outbox.clear()

        # 1. Iniciar sesión previa para verificar que se revoca tras cambiar contraseña
        login_resp = self.client.post(
            '/api/v1/auth/login/',
            {'correo': 'cliente1@plus.org', 'password': 'ClaveSegura123!'},
            format='json',
        )
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)
        old_access = login_resp.data['access']
        old_refresh = login_resp.data['refresh']

        # 2. Solicitud para correo inexistente devuelve misma respuesta genérica y no envía correo
        unknown_resp = self.client.post(
            '/api/v1/auth/password-reset/request/',
            {'correo': 'noexiste@plus.org'},
            format='json',
        )
        self.assertEqual(unknown_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)

        # 3. Solicitud para cuenta activa genera y envía correo HTML + texto con el enlace exacto
        req_resp = self.client.post(
            '/api/v1/auth/password-reset/request/',
            {'correo': 'cliente1@plus.org'},
            format='json',
        )
        self.assertEqual(req_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(req_resp.data['message'], unknown_resp.data['message'])
        self.assertEqual(len(mail.outbox), 1)

        sent_msg = mail.outbox[0]
        self.assertEqual(sent_msg.to, ['cliente1@plus.org'])
        self.assertEqual(sent_msg.from_email, 'PLUS <notificaciones@fundacionplus.site>')
        self.assertIn('PLUS', sent_msg.subject)
        self.assertIn('1 hora (60 minutos)', sent_msg.body)
        self.assertIn('ignorar este mensaje', sent_msg.body)
        self.assertEqual(len(sent_msg.alternatives), 1)
        html_content, mime_type = sent_msg.alternatives[0]
        self.assertEqual(mime_type, 'text/html')
        self.assertIn('Corporación Pluralismo Social', html_content)
        self.assertIn('ignorar este correo', html_content)

        # Extraer enlace https://fundacionplus.site/restablecer-contrasena?uid=<uid>&token=<token>
        match = re.search(
            r'https://fundacionplus\.site/restablecer-contrasena\?uid=([^&\s"\'<]+)&token=([^&\s"\'<]+)',
            sent_msg.body,
        )
        self.assertIsNotNone(match)
        uid, token = match.group(1), match.group(2)

        # 4. Solicitud repetida inmediata dentro de la ventana de enfriamiento no reenvía duplicado
        repeat_resp = self.client.post(
            '/api/v1/auth/password-reset/request/',
            {'correo': 'cliente1@plus.org'},
            format='json',
        )
        self.assertEqual(repeat_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

        # 5. Validar enlace (formato uid + token separado y formato compuesto <uid>.<token>)
        val_ok = self.client.post(
            '/api/v1/auth/password-reset/validate/',
            {'uid': uid, 'token': token},
            format='json',
        )
        self.assertEqual(val_ok.status_code, status.HTTP_200_OK)
        self.assertTrue(val_ok.data['valid'])

        val_combined = self.client.post(
            '/api/v1/auth/password-reset/validate/',
            {'token': f'{uid}.{token}'},
            format='json',
        )
        self.assertEqual(val_combined.status_code, status.HTTP_200_OK)
        self.assertTrue(val_combined.data['valid'])

        # 6. Verificar caducidad del enlace cuando supera PASSWORD_RESET_TIMEOUT
        with override_settings(PASSWORD_RESET_TIMEOUT=-1):
            expired_resp = self.client.post(
                '/api/v1/auth/password-reset/validate/',
                {'uid': uid, 'token': token},
                format='json',
            )
            self.assertEqual(expired_resp.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(expired_resp.data['code'], 'invalid_token')

        # 7. Rechazar contraseñas inválidas (corta, numérica o similar al correo del usuario)
        weak_resp = self.client.post(
            '/api/v1/auth/password-reset/confirm/',
            {'uid': uid, 'token': token, 'new_password': '12345678'},
            format='json',
        )
        self.assertEqual(weak_resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(weak_resp.data['code'], 'validation_error')

        similar_resp = self.client.post(
            '/api/v1/auth/password-reset/confirm/',
            {'uid': uid, 'token': token, 'new_password': 'cliente1@plus.org'},
            format='json',
        )
        self.assertEqual(similar_resp.status_code, status.HTTP_400_BAD_REQUEST)

        # 8. Confirmar cambio con contraseña válida
        confirm_resp = self.client.post(
            '/api/v1/auth/password-reset/confirm/',
            {
                'uid': uid,
                'token': token,
                'new_password': 'NuevaClaveFuerte2026!',
                'new_password_confirm': 'NuevaClaveFuerte2026!',
            },
            format='json',
        )
        self.assertEqual(confirm_resp.status_code, status.HTTP_200_OK)

        # 9. El enlace queda invalidado inmediatamente después de usarse
        reuse_resp = self.client.post(
            '/api/v1/auth/password-reset/confirm/',
            {'uid': uid, 'token': token, 'new_password': 'OtraClaveFuerte2026!'},
            format='json',
        )
        self.assertEqual(reuse_resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reuse_resp.data['code'], 'invalid_token')

        # 10. Las sesiones JWT anteriores (access y refresh) quedan revocadas de inmediato
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {old_access}')
        me_with_old_jwt = self.client.get('/api/v1/me/')
        self.assertEqual(me_with_old_jwt.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials()
        refresh_with_old = self.client.post(
            '/api/v1/auth/refresh/',
            {'refresh': old_refresh},
            format='json',
        )
        self.assertEqual(refresh_with_old.status_code, status.HTTP_401_UNAUTHORIZED)

        # 11. Fallo SMTP se registra en auditoría como 'fallido' sin exponer el token en logs ni en respuesta
        cache.clear()
        with patch('apps.accounts.views.send_password_reset_email', side_effect=RuntimeError('SMTP error')) as _:
            with self.assertLogs('apps.accounts.views', level='ERROR') as cm:
                fail_resp = self.client.post(
                    '/api/v1/auth/password-reset/request/',
                    {'correo': 'cliente1@plus.org'},
                    format='json',
                )
        self.assertEqual(fail_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(
            AuditAccess.objects.filter(
                correo_intentado='cliente1@plus.org',
                tipo_evento='recuperacion_clave',
                resultado='fallido',
            ).exists()
        )
        logged_text = '\n'.join(cm.output)
        self.assertNotIn(token, logged_text)

    def test_p01_and_p15_granular_rbac_and_user_management_boundaries(self):
        """P01 y P15: Separación estricta de roles e impedimento de saltarse restricciones."""
        mod_role, _ = Role.objects.get_or_create(nombre=Role.Nombre.MODERADOR)
        rep_role, _ = Role.objects.get_or_create(nombre=Role.Nombre.REPRESENTANTE)

        moderador = User.objects.create_user(
            correo='moderador@plus.org',
            password='Password123!',
            rol=mod_role,
            nombres='Marta',
            apellidos='Moderadora',
        )
        representante = User.objects.create_user(
            correo='representante@plus.org',
            password='Password123!',
            rol=rep_role,
            nombres='Roberto',
            apellidos='Representante',
        )

        mod_token = Token.objects.create(user=moderador)
        rep_token = Token.objects.create(user=representante)
        cliente_token = Token.objects.create(user=self.cliente)

        # 1. Moderador no puede acceder a gestión de usuarios, roles ni auditoría
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {mod_token.key}')
        self.assertEqual(self.client.get('/api/v1/admin/users/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get('/api/v1/admin/roles/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get('/api/v1/admin/audit-logs/').status_code, status.HTTP_403_FORBIDDEN)
        # Intento de crear usuario por moderador debe ser rechazado
        create_attempt = self.client.post(
            '/api/v1/admin/users/',
            {'correo': 'hacker@plus.org', 'password': 'Password123!', 'nombres': 'X', 'apellidos': 'Y'},
            format='json',
        )
        self.assertEqual(create_attempt.status_code, status.HTTP_403_FORBIDDEN)

        # 2. Representante tampoco puede acceder a gestión de usuarios ni roles
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {rep_token.key}')
        self.assertEqual(self.client.get('/api/v1/admin/users/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get('/api/v1/admin/roles/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get('/api/v1/admin/audit-logs/').status_code, status.HTTP_403_FORBIDDEN)

        # 3. Ciudadano no puede acceder a ningún endpoint administrativo
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {cliente_token.key}')
        self.assertEqual(self.client.get('/api/v1/admin/users/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get('/api/v1/admin/cases/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get('/api/v1/admin/roles/').status_code, status.HTTP_403_FORBIDDEN)

        # 4. Administrador sí puede gestionar usuarios
        admin_token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        users_resp = self.client.get('/api/v1/admin/users/')
        self.assertEqual(users_resp.status_code, status.HTTP_200_OK)

        # 5. Protección de auto-bloqueo del único administrador
        demote_self = self.client.put(
            f'/api/v1/admin/users/{self.admin.id}/role/',
            {'role_code': 'ciudadano', 'motivo': 'Prueba democión'},
            format='json',
        )
        self.assertEqual(demote_self.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(demote_self.data['code'], 'last_admin_lock')

    def test_p16_session_revocation_on_role_and_status_change(self):
        """P16: Revocación inmediata de sesión JWT al cambiar rol o estado."""
        # 1. Login del usuario para emitir access y refresh con 'sid'
        login_resp = self.client.post(
            '/api/v1/auth/login/',
            {'correo': 'cliente1@plus.org', 'password': 'ClaveSegura123!'},
            format='json',
        )
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)
        active_access = login_resp.data['tokens']['access']
        active_refresh = login_resp.data['tokens']['refresh']

        # Verificar que la sesión actual funciona
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {active_access}')
        me_resp = self.client.get('/api/v1/me/')
        self.assertEqual(me_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(me_resp.data['primary_role'], Role.Nombre.CIUDADANO)

        # 2. Administrador cambia el rol del usuario a 'representante'
        admin_token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        role_change_resp = self.client.put(
            f'/api/v1/admin/users/{self.cliente.id}/role/',
            {'role_code': 'representante', 'motivo': 'Ascenso a representante territorial'},
            format='json',
        )
        self.assertEqual(role_change_resp.status_code, status.HTTP_200_OK)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.get_primary_role(), Role.Nombre.REPRESENTANTE)

        # 3. La sesión anterior del usuario queda inmediatamente invalidada
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {active_access}')
        blocked_request = self.client.get('/api/v1/me/')
        self.assertEqual(blocked_request.status_code, status.HTTP_401_UNAUTHORIZED)

        # 4. El token refresh anterior también queda invalidado
        self.client.credentials()
        blocked_refresh = self.client.post(
            '/api/v1/auth/refresh/',
            {'refresh': active_refresh},
            format='json',
        )
        self.assertEqual(blocked_refresh.status_code, status.HTTP_401_UNAUTHORIZED)

        # 5. Nuevo login genera sesión fresca con el rol actualizado
        new_login = self.client.post(
            '/api/v1/auth/login/',
            {'correo': 'cliente1@plus.org', 'password': 'ClaveSegura123!'},
            format='json',
        )
        self.assertEqual(new_login.status_code, status.HTTP_200_OK)
        self.assertEqual(new_login.data['primary_role'], Role.Nombre.REPRESENTANTE)
        self.assertIn('representante', new_login.data['roles'])
