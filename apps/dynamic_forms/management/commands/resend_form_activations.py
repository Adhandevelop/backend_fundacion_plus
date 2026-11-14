from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User
from apps.dynamic_forms.models import Formulario, FormularioEnvio, FormularioNotificacion, FormularioToken
from apps.dynamic_forms.services import FormularioNotificationService, FormularioTokenService


class Command(BaseCommand):
    help = (
        'Reenvía correos de notificación o activación a las personas que respondieron formularios. '
        'Permite reintentar notificaciones fallidas o generar nuevos enlaces de activación.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default=None,
            help='Filtrar por una dirección de correo específica.',
        )
        parser.add_argument(
            '--form',
            type=str,
            default=None,
            help='Filtrar por slug o UUID de un formulario específico.',
        )
        parser.add_argument(
            '--retry-failed',
            action='store_true',
            help='Reintenta el envío de notificaciones registradas como fallidas en la base de datos.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra la lista de envíos o notificaciones a procesar sin enviar ningún correo.',
        )

    def handle(self, *args, **options):
        email_filter = options.get('email')
        form_filter = options.get('form')
        retry_failed = options.get('retry_failed')
        dry_run = options.get('dry_run')

        self.stdout.write(self.style.MIGRATE_HEADING('\n=== Reenvío de Correos para Formularios PLUS ===\n'))

        if retry_failed:
            self.handle_retry_failed(email_filter=email_filter, dry_run=dry_run)
        else:
            self.handle_pending_activations(email_filter=email_filter, form_filter=form_filter, dry_run=dry_run)

    def handle_retry_failed(self, email_filter=None, dry_run=False):
        qs = FormularioNotificacion.objects.filter(estado=FormularioNotificacion.Estado.FALLIDO)
        if email_filter:
            qs = qs.filter(correo_destino__iexact=email_filter.strip())

        total = qs.count()
        self.stdout.write(f'Notificaciones fallidas encontradas: {total}')
        if total == 0:
            self.stdout.write(self.style.SUCCESS('No hay notificaciones fallidas pendientes de reenvío.'))
            return

        if dry_run:
            self.stdout.write(self.style.WARNING('[DRY-RUN] Destinatarios que recibirían reintento:'))
            for notif in qs[:30]:
                self.stdout.write(f'  - {notif.correo_destino} (Asunto: {notif.asunto})')
            if total > 30:
                self.stdout.write(f'  ... y {total - 30} más.')
            return

        success_count = 0
        fail_count = 0
        from django.core.mail import send_mail
        from django.conf import settings

        from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'PLUS <notificaciones@fundacionplus.site>'

        for notif in qs:
            try:
                send_mail(
                    subject=notif.asunto,
                    message=notif.cuerpo_texto,
                    from_email=from_addr,
                    recipient_list=[notif.correo_destino],
                    fail_silently=False,
                )
                notif.estado = FormularioNotificacion.Estado.ENVIADO
                notif.fecha_envio = timezone.now()
                notif.save()
                success_count += 1
                self.stdout.write(self.style.SUCCESS(f'  [✓ ENVIADO] {notif.correo_destino}'))
            except Exception as exc:
                notif.intentos += 1
                notif.error_mensaje = str(exc)[:500]
                notif.save()
                fail_count += 1
                self.stdout.write(self.style.ERROR(f'  [✗ FALLÓ] {notif.correo_destino}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'\nResumen: {success_count} enviados exitosamente, {fail_count} fallidos.'))

    def handle_pending_activations(self, email_filter=None, form_filter=None, dry_run=False):
        qs = FormularioEnvio.objects.filter(
            estado_vinculacion__in=[
                FormularioEnvio.EstadoVinculacion.PENDIENTE_ACTIVACION,
                FormularioEnvio.EstadoVinculacion.PENDIENTE_REIVINDICACION,
            ]
        ).select_related('formulario', 'usuario')

        if email_filter:
            qs = qs.filter(correo_declarado__iexact=email_filter.strip())

        if form_filter:
            try:
                import uuid
                f_uuid = uuid.UUID(form_filter)
                qs = qs.filter(formulario_id=f_uuid)
            except (ValueError, TypeError):
                qs = qs.filter(formulario__slug__iexact=form_filter)

        total = qs.count()
        self.stdout.write(f'Envíos pendientes de activación encontrados: {total}')
        if total == 0:
            self.stdout.write(self.style.NOTICE(
                'No se encontraron envíos con estado pendiente_activacion / pendiente_reivindicacion.\n'
                'Si deseas reenviar a todos los envíos de un formulario (incluso ya procesados), '
                'puedes especificar el correo con --email <correo>.'
            ))
            return

        if dry_run:
            self.stdout.write(self.style.WARNING('[DRY-RUN] Envíos que recibirán nuevo correo de activación:'))
            for envio in qs[:30]:
                self.stdout.write(f'  - {envio.correo_declarado} | {envio.nombres_declarados} {envio.apellidos_declarados} | Formulario: {envio.formulario.titulo}')
            if total > 30:
                self.stdout.write(f'  ... y {total - 30} más.')
            return

        success_count = 0
        fail_count = 0

        # Agrupar por correo para evitar enviar múltiples correos redundantes al mismo ciudadano si llenó varias veces
        correos_procesados = set()

        for envio in qs.order_by('-fecha_envio'):
            norm_correo = envio.correo_declarado.strip().lower()
            if norm_correo in correos_procesados:
                continue
            correos_procesados.add(norm_correo)

            user = User.objects.filter(correo__iexact=norm_correo).first()
            proposito = (
                FormularioToken.Proposito.ACTIVAR_CUENTA
                if envio.estado_vinculacion == FormularioEnvio.EstadoVinculacion.PENDIENTE_ACTIVACION
                else FormularioToken.Proposito.REIVINDICAR_ENVIO
            )

            try:
                raw_token, token_obj = FormularioTokenService.create_token(
                    usuario=user,
                    correo=norm_correo,
                    proposito=proposito,
                    ip='127.0.0.1',
                )
                FormularioNotificationService.enqueue_activation_email(
                    envio=envio,
                    correo=norm_correo,
                    raw_token=raw_token,
                    proposito=proposito,
                )
                success_count += 1
                self.stdout.write(self.style.SUCCESS(f'  [✓ ENVIADO] {norm_correo} ({envio.formulario.titulo})'))
            except Exception as exc:
                fail_count += 1
                self.stdout.write(self.style.ERROR(f'  [✗ FALLÓ] {norm_correo}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'\nResumen: {success_count} enviados exitosamente, {fail_count} fallidos.'))
