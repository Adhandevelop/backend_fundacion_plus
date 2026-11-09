import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import escape

logger = logging.getLogger(__name__)


def build_password_reset_url(uid: str, token: str) -> str:
    base_url = getattr(settings, 'FRONTEND_URL', 'https://fundacionplus.site').strip().rstrip('/')
    return f'{base_url}/restablecer-contrasena?uid={uid}&token={token}'


def send_password_reset_email(user, uid: str, token: str) -> bool:
    """
    Envía el correo de recuperación de contraseña en formato texto plano + HTML
    mediante el backend SMTP configurado (Resend SMTP en producción).
    Nunca registra el token ni credenciales en logs.
    """
    reset_url = build_password_reset_url(uid, token)
    timeout_seconds = int(getattr(settings, 'PASSWORD_RESET_TIMEOUT', 3600) or 3600)
    timeout_minutes = max(1, round(timeout_seconds / 60))
    if timeout_minutes == 60:
        expiry_label = '1 hora (60 minutos)'
    elif timeout_minutes % 60 == 0:
        hours = timeout_minutes // 60
        expiry_label = f'{hours} horas ({timeout_minutes} minutos)'
    else:
        expiry_label = f'{timeout_minutes} minutos'

    full_name = (getattr(user, 'full_name', '') or getattr(user, 'nombres', '') or 'usuario').strip()
    safe_name = escape(full_name)
    safe_url = escape(reset_url)

    subject = 'Restablecimiento de contraseña — PLUS (Corporación Pluralismo Social)'
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'PLUS <notificaciones@fundacionplus.site>')

    text_body = (
        f'Hola {full_name},\n\n'
        'Recibimos una solicitud para restablecer la contraseña de tu cuenta en la plataforma web de '
        'PLUS (Corporación Pluralismo Social).\n\n'
        'Para crear una nueva contraseña, abre el siguiente enlace:\n'
        f'{reset_url}\n\n'
        f'Importante: Este enlace es de un solo uso y caducará en {expiry_label}.\n\n'
        'Si tú no solicitaste este cambio, puedes ignorar este mensaje con total tranquilidad; '
        'tu contraseña actual seguirá siendo válida y tu cuenta permanecerá segura.\n\n'
        'Atentamente,\n'
        'Equipo PLUS — Corporación Pluralismo Social\n'
        'https://fundacionplus.site\n'
    )

    html_body = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Restablecimiento de contraseña — PLUS</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f6f8;font-family:Arial,Helvetica,sans-serif;color:#1f2937;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#f4f6f8;padding:24px 12px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:600px;background-color:#ffffff;border-radius:8px;overflow:hidden;border:1px solid #e5e7eb;">
          <tr>
            <td style="background-color:#0f172a;padding:20px 28px;color:#ffffff;">
              <h1 style="margin:0;font-size:20px;font-weight:700;">PLUS · Corporación Pluralismo Social</h1>
            </td>
          </tr>
          <tr>
            <td style="padding:28px;">
              <p style="margin:0 0 16px 0;font-size:16px;">Hola <strong>{safe_name}</strong>,</p>
              <p style="margin:0 0 16px 0;font-size:15px;line-height:1.5;">
                Recibimos una solicitud para restablecer la contraseña de tu cuenta en la plataforma de
                <strong>PLUS (Corporación Pluralismo Social)</strong>.
              </p>
              <p style="margin:24px 0;text-align:center;">
                <a href="{safe_url}"
                   style="display:inline-block;background-color:#2563eb;color:#ffffff;text-decoration:none;padding:12px 24px;border-radius:6px;font-weight:600;font-size:15px;">
                  Restablecer mi contraseña
                </a>
              </p>
              <p style="margin:0 0 12px 0;font-size:13px;line-height:1.5;color:#4b5563;">
                Si el botón no funciona, copia y pega el siguiente enlace en tu navegador:<br>
                <a href="{safe_url}" style="color:#2563eb;word-break:break-all;">{safe_url}</a>
              </p>
              <p style="margin:16px 0;padding:12px 16px;background-color:#eff6ff;border-left:4px solid #2563eb;font-size:14px;line-height:1.5;color:#1e3a8a;">
                <strong>Caducidad:</strong> Este enlace es de un solo uso y estará vigente durante <strong>{escape(expiry_label)}</strong>.
              </p>
              <p style="margin:16px 0 0 0;font-size:14px;line-height:1.5;color:#4b5563;">
                Si no solicitaste restablecer tu contraseña, puedes <strong>ignorar este correo</strong>. No se realizará ningún cambio en tu cuenta.
              </p>
            </td>
          </tr>
          <tr>
            <td style="background-color:#f9fafb;padding:16px 28px;border-top:1px solid #e5e7eb;font-size:12px;color:#6b7280;text-align:center;">
              Corporación Pluralismo Social (PLUS) · <a href="https://fundacionplus.site" style="color:#4b5563;">fundacionplus.site</a>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[user.correo],
    )
    msg.attach_alternative(html_body, 'text/html')
    msg.send(fail_silently=False)
    return True
