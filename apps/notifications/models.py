import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    """
    Tabla SQL: plus.notificaciones
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_notificacion',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_usuario',
        related_name='notificaciones',
    )
    caso = models.ForeignKey(
        'cases.Case',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_caso',
        related_name='notificaciones',
    )
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=50, default='sistema')
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'notificaciones'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['usuario', 'leida', '-fecha_creacion'], name='ix_notificaciones_usuario'),
            models.Index(fields=['caso'], name='ix_notificaciones_caso'),
        ]

    @property
    def id_notificacion(self):
        return self.id

    def mark_as_read(self):
        if not self.leida:
            self.leida = True
            self.save(update_fields=['leida'])

    def __str__(self):
        return f'Notificación ({self.usuario.correo}): {self.titulo}'
