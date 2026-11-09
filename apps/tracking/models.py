import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class CaseUpdate(models.Model):
    """
    Tabla SQL: plus.seguimientos (Ampliada con AMP-08: titulo, audiencia y tipo_evento)
    """

    class Audiencia(models.TextChoices):
        PUBLICO = 'publico', 'Público'
        CIUDADANO = 'ciudadano', 'Ciudadano / Equipo'
        INTERNO = 'interno', 'Interno'

    class TipoEvento(models.TextChoices):
        SEGUIMIENTO = 'seguimiento', 'Seguimiento'
        RESOLUCION = 'resolucion', 'Resolución'
        CIERRE = 'cierre', 'Cierre'
        NOTA_INTERNA = 'nota_interna', 'Nota interna'
        APORTE_CIUDADANO = 'aporte_ciudadano', 'Aporte ciudadano'

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
    titulo = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.TextField()
    audiencia = models.CharField(
        max_length=20,
        choices=Audiencia.choices,
        default=Audiencia.INTERNO,
    )
    tipo_evento = models.CharField(
        max_length=30,
        choices=TipoEvento.choices,
        default=TipoEvento.SEGUIMIENTO,
    )
    fecha_seguimiento = models.DateTimeField(default=timezone.now)
    visible_publicamente = models.BooleanField(default=False)

    class Meta:
        db_table = 'seguimientos'
        ordering = ['-fecha_seguimiento']
        indexes = [
            models.Index(fields=['caso', '-fecha_seguimiento'], name='ix_seguimientos_caso_fecha'),
        ]

    def save(self, *args, **kwargs):
        # Si se indicó explícitamente visible_publicamente=True y audiencia sigue en default, elevar a 'publico'
        if self.visible_publicamente and self.audiencia == self.Audiencia.INTERNO:
            self.audiencia = self.Audiencia.PUBLICO
        # Sincronizar visible_publicamente desde audiencia (regla AMP-08: una sola fuente de verdad)
        self.visible_publicamente = self.audiencia == self.Audiencia.PUBLICO
        super().save(*args, **kwargs)

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
        indexes = [
            models.Index(fields=['caso', '-fecha_cambio'], name='ix_historial_caso_fecha'),
        ]

    @property
    def id_historial(self):
        return self.id

    def __str__(self):
        ant = self.estado_anterior.nombre if self.estado_anterior else 'NULL'
        return f'{self.caso.codigo}: {ant} -> {self.estado_nuevo.nombre}'
