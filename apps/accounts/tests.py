import re
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User
from apps.audit.models import AuditAccess, AuditLog, AuditPermission
from apps.communications.models import SiteSetting


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


class SuperadminHomeHeroTests(APITestCase):
    """
    Pruebas integrales para la gestión exclusiva de la fotografía principal de inicio (Hero Image):
    - Distinción entre superadministrador y administrador normal.
    - Exposición de can_manage_homepage en /me/ y permissions.
    - Acceso a GET /api/v1/admin/site/home-hero/.
    - Reemplazo mediante PUT /api/v1/admin/site/home-hero/ con validación binaria (<= 5MB, JPG/PNG/WEBP).
    - 403 Forbidden para administradores normales, moderadores, representantes y ciudadanos.
    - Validación y conservación de la imagen anterior en caso de fallo.
    - Registro de auditoría (AuditLog).
    - Disponibilidad pública en /api/v1/public/site/ y /api/v1/public/home/.
    """

    def setUp(self):
        # Rol administrador y ciudadano
        self.admin_role, _ = Role.objects.get_or_create(nombre=Role.Nombre.ADMINISTRADOR)
        self.citizen_role, _ = Role.objects.get_or_create(nombre=Role.Nombre.CIUDADANO)

        # Superadministrador (email admin@plus.org registrado en SUPERADMIN_EMAILS)
        self.superadmin = User.objects.create_user(
            username='superadmin',
            email='admin@plus.org',
            password='SuperPassword123!',
            rol=self.admin_role,
            is_staff=True,
        )

        # Administrador general/normal (no está en SUPERADMIN_EMAILS)
        self.normal_admin = User.objects.create_user(
            username='admin_normal',
            email='gestor_general@plus.org',
            password='NormalAdmin123!',
            rol=self.admin_role,
            is_staff=True,
        )

        # Ciudadano
        self.ciudadano = User.objects.create_user(
            username='ciudadano_test',
            email='vecino@plus.org',
            password='Ciudadano123!',
            rol=self.citizen_role,
        )

        # Configuración inicial de Hero
        self.hero_setting, _ = SiteSetting.objects.get_or_create(
            clave='INSTITUTION_HERO',
            defaults={
                'valor': {
                    'image_url': '/media/site/hero/initial.jpg?v=1',
                    'alt_text': 'Fotografía inicial de la sede PLUS',
                    'version': '1',
                }
            },
        )

    def test_can_manage_homepage_exposed_in_me_and_permissions(self):
        # Superadministrador
        self.client.force_authenticate(user=self.superadmin)
        res_super = self.client.get('/api/v1/me/')
        self.assertEqual(res_super.status_code, status.HTTP_200_OK)
        self.assertTrue(res_super.data.get('can_manage_homepage'))
        self.assertTrue(res_super.data['permissions'].get('can_manage_homepage'))

        # Administrador normal
        self.client.force_authenticate(user=self.normal_admin)
        res_normal = self.client.get('/api/v1/me/')
        self.assertEqual(res_normal.status_code, status.HTTP_200_OK)
        self.assertFalse(res_normal.data.get('can_manage_homepage'))
        self.assertFalse(res_normal.data['permissions'].get('can_manage_homepage'))

        # Ciudadano
        self.client.force_authenticate(user=self.ciudadano)
        res_ciu = self.client.get('/api/v1/me/')
        self.assertEqual(res_ciu.status_code, status.HTTP_200_OK)
        self.assertFalse(res_ciu.data.get('can_manage_homepage'))
        self.assertFalse(res_ciu.data['permissions'].get('can_manage_homepage'))

    def test_superadmin_can_get_and_put_home_hero_with_audit_and_versioning(self):
        self.client.force_authenticate(user=self.superadmin)

        # GET hero actual
        get_res = self.client.get('/api/v1/admin/site/home-hero/')
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data['alt_text'], 'Fotografía inicial de la sede PLUS')

        # PUT nueva imagen JPEG válida con magic bytes
        valid_jpeg_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00' + b'A' * 200
        image_file = SimpleUploadedFile('nuevo_hero.jpg', valid_jpeg_content, content_type='image/jpeg')

        put_res = self.client.put(
            '/api/v1/admin/site/home-hero/',
            {
                'image': image_file,
                'alt_text': 'Comunidad Unida de Villavicencio y Meta',
            },
            format='multipart',
        )
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.assertEqual(put_res.data['alt_text'], 'Comunidad Unida de Villavicencio y Meta')
        self.assertIn('?v=', put_res.data['image_url'])
        self.assertIn('/media/site/hero/', put_res.data['image_url'])

        # Verificar auditoría
        audit_entry = AuditLog.objects.filter(
            modulo='configuracion_sitio',
            accion='update',
            usuario=self.superadmin,
        ).first()
        self.assertIsNotNone(audit_entry)
        self.assertEqual(audit_entry.modulo, 'configuracion_sitio')
        self.assertIn('Hero Image', audit_entry.datos_nuevos.get('descripcion', ''))

    def test_normal_admin_and_other_roles_forbidden(self):
        valid_jpeg_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00' + b'A' * 200

        # Normal admin recibe 403 Forbidden en GET y PUT
        self.client.force_authenticate(user=self.normal_admin)
        res_get_normal = self.client.get('/api/v1/admin/site/home-hero/')
        self.assertEqual(res_get_normal.status_code, status.HTTP_403_FORBIDDEN)

        image_file = SimpleUploadedFile('intruso.jpg', valid_jpeg_content, content_type='image/jpeg')
        res_put_normal = self.client.put(
            '/api/v1/admin/site/home-hero/',
            {'image': image_file, 'alt_text': 'Intento no autorizado'},
            format='multipart',
        )
        self.assertEqual(res_put_normal.status_code, status.HTTP_403_FORBIDDEN)

        # Ciudadano recibe 403 Forbidden
        self.client.force_authenticate(user=self.ciudadano)
        image_file2 = SimpleUploadedFile('intruso2.jpg', valid_jpeg_content, content_type='image/jpeg')
        res_put_ciu = self.client.put(
            '/api/v1/admin/site/home-hero/',
            {'image': image_file2, 'alt_text': 'Intento ciudadano'},
            format='multipart',
        )
        self.assertEqual(res_put_ciu.status_code, status.HTTP_403_FORBIDDEN)

        # Sin autenticación recibe 401 Unauthorized
        self.client.credentials()
        self.client.logout()
        res_anon = self.client.get('/api/v1/admin/site/home-hero/')
        self.assertEqual(res_anon.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_file_rejected_and_previous_image_preserved(self):
        self.client.force_authenticate(user=self.superadmin)

        # Archivo con extensión permitida pero contenido inválido (sin magic bytes)
        fake_image = SimpleUploadedFile('malicioso.jpg', b'ESTO NO ES UN JPEG BINARIO VALIDO', content_type='image/jpeg')
        res = self.client.put(
            '/api/v1/admin/site/home-hero/',
            {'image': fake_image, 'alt_text': 'Texto fallido'},
            format='multipart',
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # La imagen anterior debe conservarse intacta
        self.hero_setting.refresh_from_db()
        self.assertEqual(self.hero_setting.valor['alt_text'], 'Fotografía inicial de la sede PLUS')

    def test_oversized_file_rejected(self):
        self.client.force_authenticate(user=self.superadmin)

        # Archivo mayor a 5 MB (5.1 MB con magic bytes JPEG)
        oversized = SimpleUploadedFile(
            'pesada.jpg',
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00' + (b'0' * (5 * 1024 * 1024 + 100)),
            content_type='image/jpeg',
        )
        res = self.client.put(
            '/api/v1/admin/site/home-hero/',
            {'image': oversized, 'alt_text': 'Foto gigante'},
            format='multipart',
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('límite acordado de 5 MB', str(res.data))

    def test_normal_admin_cannot_bypass_via_admin_site_settings(self):
        self.client.force_authenticate(user=self.normal_admin)

        # Intento de modificar INSTITUTION_HERO a través de /api/v1/admin/settings/{id}/
        res = self.client.patch(
            f'/api/v1/admin/settings/{self.hero_setting.pk}/',
            {'valor': {'image_url': '/hacked.jpg', 'alt_text': 'Bypassed'}},
            format='json',
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_endpoints_reflect_hero_image(self):
        # 1. Configurar un hero oficial con superadmin
        self.client.force_authenticate(user=self.superadmin)
        valid_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + b'B' * 100
        image_file = SimpleUploadedFile('portada_oficial.png', valid_png, content_type='image/png')
        self.client.put(
            '/api/v1/admin/site/home-hero/',
            {'image': image_file, 'alt_text': 'Sede Principal Villavicencio Meta'},
            format='multipart',
        )

        # 2. Consulta pública anónima de /api/v1/public/site/
        self.client.credentials()
        self.client.logout()

        pub_site_res = self.client.get('/api/v1/public/site/')
        self.assertEqual(pub_site_res.status_code, status.HTTP_200_OK)
        site_hero = pub_site_res.data['configuracion']['INSTITUTION_HERO']
        self.assertEqual(site_hero['alt_text'], 'Sede Principal Villavicencio Meta')
        self.assertIn('?v=', site_hero['image_url'])

        # 3. Consulta pública anónima de /api/v1/public/home/
        pub_home_res = self.client.get('/api/v1/public/home/')
        self.assertEqual(pub_home_res.status_code, status.HTTP_200_OK)
        inst_data = pub_home_res.data['institution']
        self.assertEqual(inst_data['alt_text'], 'Sede Principal Villavicencio Meta')
        self.assertIn('?v=', inst_data['image_url'])


class AdditionalIntegrationPointsTests(APITestCase):
    """Pruebas para verificar las correcciones de P01, P10, P15, P17, P19."""

    def setUp(self):
        user_model = get_user_model()
        self.rol_admin, _ = Role.objects.get_or_create(nombre=Role.Nombre.ADMINISTRADOR)
        self.rol_ciudadano, _ = Role.objects.get_or_create(nombre=Role.Nombre.CIUDADANO)
        self.rol_rep, _ = Role.objects.get_or_create(nombre=Role.Nombre.REPRESENTANTE)

        self.admin = user_model.objects.create_user(
            username='solo_admin',
            email='solo_admin@plus.org',
            password='ClaveAdmin123!',
            rol=self.rol_admin,
            estado=User.Estado.ACTIVO,
            is_staff=True,
        )
        self.ciudadano = user_model.objects.create_user(
            username='ciudadano_test',
            email='ciudadano_test@plus.org',
            password='ClaveCiudadano123!',
            rol=self.rol_ciudadano,
            estado=User.Estado.ACTIVO,
        )

    def test_p15_last_admin_lock_on_status_change_and_role(self):
        self.client.force_authenticate(user=self.admin)

        # 1. Intentar desactivar al único admin activo -> debe fallar con last_admin_lock
        res = self.client.patch(
            f'/api/v1/admin/users/{self.admin.id}/status/',
            {'estado': 'inactivo', 'motivo': 'Prueba'},
            format='json',
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data.get('code'), 'last_admin_lock')

        # 2. Intentar cambiar rol del único admin activo -> debe fallar con last_admin_lock
        res_rol = self.client.put(
            f'/api/v1/admin/users/{self.admin.id}/role/',
            {'role_code': 'ciudadano', 'motivo': 'Prueba rol'},
            format='json',
        )
        self.assertEqual(res_rol.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_rol.data.get('code'), 'last_admin_lock')

        # 3. Intentar eliminar al único admin activo -> debe fallar con last_admin_lock
        res_del = self.client.delete(f'/api/v1/admin/users/{self.admin.id}/')
        self.assertEqual(res_del.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_del.data.get('code'), 'last_admin_lock')

    def test_p10_candidate_filter_with_nonexistent_case_returns_400(self):
        self.client.force_authenticate(user=self.admin)
        import uuid
        fake_uuid = str(uuid.uuid4())
        res = self.client.get(f'/api/v1/admin/users/?eligible_for_case={fake_uuid}')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('eligible_for_case', res.data.get('errors', {}))

    def test_p01_citizen_only_rejects_admin_on_citizen_cases_and_dashboard(self):
        self.client.force_authenticate(user=self.admin)

        # Las rutas ciudadanas deben retornar 403 para administradores
        self.assertEqual(self.client.get('/api/v1/citizen/cases/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get('/api/v1/citizen/dashboard/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get('/api/v1/me/cases/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get('/api/v1/me/dashboard/').status_code, status.HTTP_403_FORBIDDEN)

        # Y retornar 200 para ciudadano activo
        self.client.force_authenticate(user=self.ciudadano)
        self.assertEqual(self.client.get('/api/v1/citizen/cases/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/citizen/dashboard/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/me/cases/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/me/dashboard/').status_code, status.HTTP_200_OK)

    def test_p17_admin_can_retrieve_frozen_form_version_with_questions(self):
        from apps.dynamic_forms.models import Formulario, FormularioPregunta, FormularioVersion
        self.client.force_authenticate(user=self.admin)
        form = Formulario.objects.create(
            slug='form-test-versions',
            titulo='Formulario de Prueba Versiones',
            creado_por=self.admin,
        )
        version = FormularioVersion.objects.create(
            formulario=form,
            numero_version=1,
            titulo_congelado='Versión 1 Congelada',
            es_vigente=True,
        )
        FormularioPregunta.objects.create(
            version=version,
            codigo='p1_nombre',
            enunciado='¿Cuál es tu nombre completo?',
            tipo_campo=FormularioPregunta.TipoCampo.TEXTO_CORTO,
            orden=1,
        )

        res = self.client.get(f'/api/v1/admin/forms/{form.id}/versions/1/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['numero_version'], 1)
        self.assertEqual(len(res.data['preguntas']), 1)
        self.assertEqual(res.data['preguntas'][0]['codigo'], 'p1_nombre')

    def test_p19_public_initiative_detail_does_not_leak_responsable_or_cases(self):
        from apps.initiatives.models import Initiative, InitiativeActivity, InitiativeEdition
        ini = Initiative.objects.create(
            titulo='Iniciativa Pública Segura',
            slug='iniciativa-publica-segura',
            descripcion='Descripción pública',
            creador=self.admin,
            estado_publicacion=Initiative.EstadoPublicacion.PUBLICADA,
        )
        ed = InitiativeEdition.objects.create(
            iniciativa=ini,
            anio=2026,
            nombre_edicion='Edición 2026',
        )
        InitiativeActivity.objects.create(
            edicion=ed,
            titulo='Taller comunitario',
            descripcion='Taller público',
            responsable=self.admin,
            lugar='Villavicencio',
        )

        # Consulta anónima
        self.client.logout()
        self.client.credentials()
        res = self.client.get(f'/api/v1/public/initiatives/{ini.slug}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ediciones = res.data.get('ediciones', [])
        self.assertTrue(len(ediciones) > 0)
        actividades = ediciones[0].get('actividades', [])
        self.assertTrue(len(actividades) > 0)
        act = actividades[0]
        # Verificar ausencia de campos sensibles
        self.assertNotIn('responsable', act)
        self.assertNotIn('responsable_nombre', act)
        self.assertNotIn('ubicacion', act)
        self.assertNotIn('casos_vinculados', ediciones[0])

    def test_p12_audit_event_pagination_and_uniform_filters(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get('/api/v1/admin/audit-events/?page=1&page_size=10')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('count', res.data)
        self.assertIn('page', res.data)
        self.assertIn('page_size', res.data)
        self.assertIn('total_pages', res.data)
        self.assertIn('results', res.data)
        self.assertIn('kpis', res.data)

    def test_p20_initiative_editorial_lifecycle_and_subresource_audit(self):
        from apps.initiatives.models import Initiative
        self.client.force_authenticate(user=self.admin)
        ini = Initiative.objects.create(
            titulo='Programa Prueba P20',
            slug='programa-prueba-p20',
            creador=self.admin,
            estado_publicacion=Initiative.EstadoPublicacion.BORRADOR,
        )
        # 1. Publicar mediante acción atómica
        res_pub = self.client.post(f'/api/v1/admin/initiatives/{ini.id}/publish/')
        self.assertEqual(res_pub.status_code, status.HTTP_200_OK)
        ini.refresh_from_db()
        self.assertEqual(ini.estado_publicacion, Initiative.EstadoPublicacion.PUBLICADA)

        # 2. Archivar mediante acción atómica
        res_arch = self.client.post(f'/api/v1/admin/initiatives/{ini.id}/archive/')
        self.assertEqual(res_arch.status_code, status.HTTP_200_OK)
        ini.refresh_from_db()
        self.assertEqual(ini.estado, Initiative.Estado.FINALIZADA)

    def test_p21_multipart_media_upload_news_and_initiatives(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        from apps.news.models import NewsArticle, NewsCategory
        from apps.initiatives.models import Initiative

        self.client.force_authenticate(user=self.admin)
        cat = NewsCategory.objects.create(nombre='Categoría P21', slug='cat-p21')
        article = NewsArticle.objects.create(
            titulo='Noticia Multimedia P21',
            slug='noticia-multimedia-p21',
            extracto='Extracto',
            contenido='Contenido',
            autor=self.admin,
            categoria=cat,
        )
        ini = Initiative.objects.create(
            titulo='Iniciativa Multimedia P21',
            slug='iniciativa-multimedia-p21',
            creador=self.admin,
        )

        valid_jpg = SimpleUploadedFile(
            'foto_campo.jpg',
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\x60\x00\x60\x00\x00\xff\xdb\x00C\x00',
            content_type='image/jpeg',
        )

        # 1. Subida válida a noticias SIN enviar ruta_archivo
        res_news = self.client.post(
            '/api/v1/admin/news-media/',
            {
                'noticia': str(article.id),
                'file': valid_jpg,
                'texto_alternativo': 'Foto comunitaria',
                'es_portada': True,
            },
            format='multipart',
        )
        self.assertEqual(res_news.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', res_news.data)
        self.assertIn('ruta_archivo', res_news.data)
        self.assertTrue(res_news.data['ruta_archivo'].startswith('news/'))
        self.assertIn('url', res_news.data)
        self.assertIn('/api/v1/public/media/news/', res_news.data['url'])

        # 2. Subida válida a iniciativas SIN enviar ruta_archivo
        valid_png = SimpleUploadedFile(
            'grafico_avance.png',
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + b'0' * 50,
            content_type='image/png',
        )
        res_ini = self.client.post(
            '/api/v1/admin/initiative-media/',
            {
                'iniciativa': str(ini.id),
                'file': valid_png,
                'texto_alternativo': 'Gráfico de avance',
                'es_portada': True,
            },
            format='multipart',
        )
        self.assertEqual(res_ini.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', res_ini.data)
        self.assertIn('ruta_archivo', res_ini.data)
        self.assertTrue(res_ini.data['ruta_archivo'].startswith('initiatives/'))
        self.assertIn('url', res_ini.data)
        self.assertIn('/api/v1/public/media/initiatives/', res_ini.data['url'])

        # 3. Formato no permitido (.exe o .txt)
        bad_file = SimpleUploadedFile('script.exe', b'MZ12345', content_type='application/x-msdownload')
        res_bad = self.client.post(
            '/api/v1/admin/news-media/',
            {'noticia': str(article.id), 'file': bad_file},
            format='multipart',
        )
        self.assertEqual(res_bad.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file', str(res_bad.data))

        # 4. Archivo mayor a 15 MB
        big_file = SimpleUploadedFile('pesado.jpg', b'0' * (15 * 1024 * 1024 + 10), content_type='image/jpeg')
        res_big = self.client.post(
            '/api/v1/admin/news-media/',
            {'noticia': str(article.id), 'file': big_file},
            format='multipart',
        )
        self.assertEqual(res_big.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('15 MB', str(res_big.data))

        # 5. Petición sin archivo ni ruta_archivo
        res_empty = self.client.post(
            '/api/v1/admin/news-media/',
            {'noticia': str(article.id), 'texto_alternativo': 'Sin archivo'},
            format='multipart',
        )
        self.assertEqual(res_empty.status_code, status.HTTP_400_BAD_REQUEST)



