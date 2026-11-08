import uuid
from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class CaseUpdate(models.Model):
    """
    Tabla SQL: plus.seguimientos
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_seguimiento',
    )
    caso = models.ForeignKey(
        'cases.Case',
        on_delete=models.RESTRICT,
        db_column='id_caso',
        related_name='seguimientos',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_usuario',
        related_name='seguimientos_registrados',
    )
    descripcion = models.TextField()
    fecha_seguimiento = models.DateTimeField(default=timezone.now)
    visible_publicamente = models.BooleanField(default=False)

    class Meta:
        db_table = 'seguimientos'
        ordering = ['-fecha_seguimiento']
        indexes = [
            models.Index(fields=['caso', '-fecha_seguimiento'], name='ix_seguimientos_caso_fecha'),
        ]

    @property
    def id_seguimiento(self):
        return self.id

    def __str__(self):
        return f'Seguimiento {self.caso.codigo} ({self.fecha_seguimiento})'


class CaseStatusHistory(models.Model):
    """
    Tabla SQL: plus.historial_estados
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_historial',
    )
    caso = models.ForeignKey(
        'cases.Case',
        on_delete=models.RESTRICT,
        db_column='id_caso',
        related_name='historial_estados',
    )
    estado_anterior = models.ForeignKey(
        'cases.CaseStatus',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_estado_anterior',
        related_name='historiales_como_anterior',
    )
    estado_nuevo = models.ForeignKey(
        'cases.CaseStatus',
        on_delete=models.RESTRICT,
        db_column='id_estado_nuevo',
        related_name='historiales_como_nuevo',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='cambios_estado_registrados',
    )
    motivo = models.TextField(null=True, blank=True)
    fecha_cambio = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'historial_estados'
        ordering = ['-fecha_cambio']
        constraints = [
            models.CheckConstraint(
                check=Q(estado_anterior__isnull=True) | ~Q(estado_anterior=F('estado_nuevo')),
                name='ck_historial_distinto',
            ),
        ]
        indexes = [
            models.Index(fields=['caso', '-fecha_cambio'], name='ix_historial_caso_fecha'),
        ]

    @property
    def id_historial(self):
        return self.id

    def __str__(self):
        ant = self.estado_anterior.nombre if self.estado_anterior else 'NULL'
        return f'{self.caso.codigo}: {ant} -> {self.estado_nuevo.nombre}'
