from apps.notifications.models import Notification


class NotificationService:
    @staticmethod
    def notify(*, recipient, notification_type: str, title: str, message: str, related_case=None, **kwargs) -> Notification:
        return Notification.objects.create(
            usuario=recipient,
            caso=related_case,
            titulo=title[:150],
            mensaje=message,
            tipo=notification_type[:50],
            leida=False,
        )
