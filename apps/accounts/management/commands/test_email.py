import sys
import traceback
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Diagnostica la configuración de correo y prueba el envío SMTP (Resend / Django mail).'

    def add_arguments(self, parser):
        parser.add_argument(
            'recipient',
            nargs='?',
            default=None,
            help='Dirección de correo de destino para la prueba (ej: usuario@ejemplo.com)',
        )
        parser.add_argument(
            '--check-only',
            action='store_true',
            help='Solo inspecciona las variables de configuración sin intentar enviar correo.',
        )

    def handle(self, *args, **options):
        recipient = options.get('recipient')
        check_only = options.get('check_only')

        self.stdout.write(self.style.MIGRATE_HEADING('\n=== Diagnóstico de Configuración de Correo PLUS ===\n'))

        backend = getattr(settings, 'EMAIL_BACKEND', '')
        host = getattr(settings, 'EMAIL_HOST', '')
        port = getattr(settings, 'EMAIL_PORT', '')
        use_tls = getattr(settings, 'EMAIL_USE_TLS', False)
        use_ssl = getattr(settings, 'EMAIL_USE_SSL', False)
        user = getattr(settings, 'EMAIL_HOST_USER', '')
        password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        timeout = getattr(settings, 'EMAIL_TIMEOUT', 15)

        # Enmascarar contraseña
        if not password:
            pwd_display = self.style.ERROR('[NO CONFIGURADA / VACÍA]')
        elif password == 'CLAVE_REAL_CONFIGURADA_EN_EL_SERVIDOR':
            pwd_display = self.style.ERROR('[ADVERTENCIA: VALOR DE PLANTILLA NO REEMPLAZADO]')
        elif len(password) > 8:
            pwd_display = f'{password[:4]}****{password[-4:]} (longitud: {len(password)})'
        else:
            pwd_display = '**** (longitud: ' + str(len(password)) + ')'

        self.stdout.write(f'  EMAIL_BACKEND:       {backend}')
        self.stdout.write(f'  EMAIL_HOST:          {host}')
        self.stdout.write(f'  EMAIL_PORT:          {port}')
        self.stdout.write(f'  EMAIL_USE_TLS:       {use_tls}')
        self.stdout.write(f'  EMAIL_USE_SSL:       {use_ssl}')
        self.stdout.write(f'  EMAIL_HOST_USER:     {user}')
        self.stdout.write(f'  EMAIL_HOST_PASSWORD: {pwd_display}')
        self.stdout.write(f'  DEFAULT_FROM_EMAIL:  {from_email}')
        self.stdout.write(f'  EMAIL_TIMEOUT:       {timeout}s\n')

        # Verificaciones de sanidad
        warnings = []
        if 'console' in backend.lower():
            warnings.append(
                'EMAIL_BACKEND está configurado en "console". Los correos NO saldrán por internet; '
                'se imprimen únicamente en la terminal/logs del contenedor.'
            )
        if use_tls and use_ssl:
            warnings.append(
                'EMAIL_USE_TLS y EMAIL_USE_SSL son ambos True. Django requiere que solo uno de ellos sea True.'
            )
        if not password or password == 'CLAVE_REAL_CONFIGURADA_EN_EL_SERVIDOR':
            warnings.append(
                'EMAIL_HOST_PASSWORD no tiene una API key real. Para Resend SMTP, debes ingresar una API key '
                'válida que comience con "re_..." creada en https://resend.com/api-keys.'
            )

        if warnings:
            self.stdout.write(self.style.WARNING('--- Advertencias de Configuración ---'))
            for w in warnings:
                self.stdout.write(self.style.WARNING(f'  [!] {w}'))
            self.stdout.write('')

        if check_only:
            self.stdout.write(self.style.SUCCESS('[OK] Verificación completada (--check-only).'))
            return

        if not recipient:
            self.stdout.write(self.style.NOTICE(
                'Para enviar un correo de prueba, ejecuta:\n'
                '  python manage.py test_email tu-correo@ejemplo.com\n'
                'O si estás en Docker:\n'
                '  docker compose exec backend python manage.py test_email tu-correo@ejemplo.com\n'
            ))
            return

        self.stdout.write(f'Intentando enviar correo de prueba a: {self.style.WARNING(recipient)} ...')

        subject = 'Prueba de envío de correo — Plataforma PLUS'
        text_content = (
            'Hola,\n\n'
            'Este es un mensaje de prueba enviado desde la plataforma PLUS (Corporación Pluralismo Social) '
            'para verificar la conectividad SMTP con Resend.\n\n'
            'Si estás leyendo esto, el servidor de correo saliente está funcionando correctamente.\n'
        )
        html_content = (
            '<html><body>'
            '<h2 style="color:#0f172a;">Plataforma PLUS · Prueba SMTP</h2>'
            '<p>Este es un correo de prueba para verificar que el servicio de correo saliente está operativo.</p>'
            '<p style="color:#2563eb;"><strong>¡Conectividad SMTP verificada exitosamente!</strong></p>'
            '</body></html>'
        )

        try:
            connection = get_connection(fail_silently=False)
            connection.open()
            self.stdout.write(self.style.SUCCESS('  [✓] Conexión TCP/TLS con el servidor SMTP establecida.'))

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[recipient],
                connection=connection,
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send(fail_silently=False)
            connection.close()

            self.stdout.write(self.style.SUCCESS(f'\n[✓ ÉXITO] Correo de prueba enviado a {recipient}.'))
            self.stdout.write('Revisa tu bandeja de entrada y la carpeta de spam o correo no deseado.\n')

        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'\n[✗ ERROR] Falló el envío del correo de prueba: {exc.__class__.__name__}'))
            self.stdout.write(self.style.ERROR(f'Detalle: {exc}\n'))

            exc_str = str(exc).lower()
            cls_name = exc.__class__.__name__

            self.stdout.write(self.style.MIGRATE_HEADING('--- Guía de Diagnóstico y Solución ---'))

            if 'authentication' in cls_name.lower() or '535' in exc_str:
                self.stdout.write(self.style.WARNING(
                    '1. ERROR DE AUTENTICACIÓN (535):\n'
                    '   - Resend rechazó las credenciales.\n'
                    '   - Asegúrate de que EMAIL_HOST_USER="resend".\n'
                    '   - Asegúrate de que EMAIL_HOST_PASSWORD sea una API key válida creada en https://resend.com/api-keys '
                    '     (comienza con "re_...").\n'
                    '   - Si la API key tiene permisos restringidos, asegúrate de que tenga permiso de "Sending access".'
                ))
            elif 'domain' in exc_str or 'not verified' in exc_str or '451' in exc_str or '550' in exc_str:
                self.stdout.write(self.style.WARNING(
                    '2. ERROR DE DOMINIO NO VERIFICADO:\n'
                    '   - Resend requiere que el remitente pertenezca a un dominio verificado con registros DNS (SPF, DKIM).\n'
                    '   - Si tu dominio "fundacionplus.site" aún no está verificado en https://resend.com/domains:\n'
                    '     * Para pruebas inmediatas, puedes configurar temporalmente:\n'
                    '       DEFAULT_FROM_EMAIL=onboarding@resend.dev\n'
                    '     * Nota: onboarding@resend.dev solo permite enviar al correo con el que te registraste en Resend.\n'
                    '   - Para producción, ingresa a resend.com/domains y añade los registros DNS (MX, TXT SPF, DKIM) en tu proveedor DNS.'
                ))
            elif 'timeout' in exc_str or 'timed out' in exc_str or 'refused' in exc_str or 'connection' in exc_str:
                self.stdout.write(self.style.WARNING(
                    '3. ERROR DE CONEXIÓN O TIMEOUT:\n'
                    '   - Muchos proveedores de VPS (DigitalOcean, AWS, Linode, Hetzner, etc.) bloquean el puerto 587 por defecto.\n'
                    '   - Prueba cambiar a puerto 465 con SSL en tu archivo .env:\n'
                    '       EMAIL_PORT=465\n'
                    '       EMAIL_USE_SSL=True\n'
                    '       EMAIL_USE_TLS=False\n'
                    '   - Luego reinicia el contenedor con: docker compose up -d backend'
                ))
            elif 'console' in backend.lower():
                self.stdout.write(self.style.WARNING(
                    '4. BACKEND EN CONSOLA:\n'
                    '   - EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend.\n'
                    '   - En tu archivo .env del servidor debes colocar:\n'
                    '       EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Traza completa:\n{traceback.format_exc()}'
                ))

            sys.exit(1)
