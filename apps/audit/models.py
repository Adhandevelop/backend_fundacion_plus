import uuid
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils import timezone


class ImmutableAuditModel(models.Model):
    """Base abstracta que impide modificar o eliminar registros de auditoría desde la aplicación."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self._state.adding and self.__class__.objects.filter(pk=self.pk).exists():
            raise PermissionDenied('Los registros de auditoría son inmutables y no pueden modificarse.')
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionDenied('Los registros de auditoría son inmutables y no pueden eliminarse.')


class AuditLog(ImmutableAuditModel):
    """
    Tabla SQL: plus.auditoria_eventos
    """

    class Resultado(models.TextChoices):
        EXITOSO = 'exitoso', 'Exitoso'
        FALLIDO = 'fallido', 'Fallido'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_auditoria',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='auditoria_eventos',
    )
    accion = models.CharField(max_length=100)
    modulo = models.CharField(max_length=100)
    tabla_afectada = models.CharField(max_length=100, null=True, blank=True)
    id_registro = models.UUIDField(null=True, blank=True)
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    fecha_evento = models.DateTimeField(default=timezone.now)
    resultado = models.CharField(
        max_length=20,
        choices=Resultado.choices,
        default=Resultado.EXITOSO,
    )

    class Meta:
        db_table = 'auditoria_eventos'
        ordering = ['-fecha_evento']
        indexes = [
            models.Index(fields=['usuario', '-fecha_evento'], name='ix_auditoria_eventos_usr_fec'),
            models.Index(fields=['tabla_afectada', '-fecha_evento'], name='ix_auditoria_eventos_tbl_fec'),
        ]

    def __str__(self):
        return f'[{self.fecha_evento}] {self.accion} en {self.tabla_afectada or self.modulo}'


class AuditAccess(ImmutableAuditModel):
    """
    Tabla SQL: plus.auditoria_accesos
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_acceso',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='auditoria_accesos',
    )
    correo_intentado = models.CharField(max_length=150, null=True, blank=True)
    tipo_evento = models.CharField(max_length=50)
    resultado = models.CharField(max_length=20, default='exitoso')
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    fecha_evento = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'auditoria_accesos'
        ordering = ['-fecha_evento']
        indexes = [
            models.Index(fields=['-fecha_evento'], name='ix_auditoria_accesos_fecha'),
        ]


class AuditCase(ImmutableAuditModel):
    """
    Tabla SQL: plus.auditoria_casos
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_auditoria_caso',
    )
    caso = models.ForeignKey(
        'cases.Case',
        on_delete=models.RESTRICT,
        db_column='id_caso',
        related_name='auditoria_casos',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='auditoria_casos_realizados',
    )
    tipo_accion = models.CharField(max_length=100)
    estado_anterior = models.CharField(max_length=50, null=True, blank=True)
    estado_nuevo = models.CharField(max_length=50, null=True, blank=True)
    motivo = models.TextField(null=True, blank=True)
    fecha_accion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'auditoria_casos'
        ordering = ['-fecha_accion']
        indexes = [
            models.Index(fields=['caso', '-fecha_accion'], name='ix_auditoria_casos_caso_fecha'),
        ]


class AuditPermission(ImmutableAuditModel):
    """
    Tabla SQL: plus.auditoria_permisos
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_auditoria_permiso',
    )
    usuario_afectado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_usuario_afectado',
        related_name='auditoria_permisos_recibidos',
    )
    usuario_responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario_responsable',
        related_name='auditoria_permisos_otorgados',
    )
    tipo_cambio = models.CharField(max_length=100)
    valor_anterior = models.JSONField(null=True, blank=True)
    valor_nuevo = models.JSONField(null=True, blank=True)
    motivo = models.TextField(null=True, blank=True)
    fecha_cambio = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'auditoria_permisos'
        ordering = ['-fecha_cambio']
        indexes = [
            models.Index(fields=['usuario_afectado', '-fecha_cambio'], name='ix_auditoria_permisos_usr_fec'),
        ]


class AuditSecurity(ImmutableAuditModel):
    """
    Tabla SQL: plus.auditoria_seguridad
    """

    class Severidad(models.TextChoices):
        BAJO = 'bajo', 'Bajo'
        MEDIO = 'medio', 'Medio'
        ALTO = 'alto', 'Alto'
        CRITICO = 'critico', 'Crítico'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_evento_seguridad',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='auditoria_seguridad',
    )
    tipo_evento = models.CharField(max_length=100)
    nivel_severidad = models.CharField(
        max_length=20,
        choices=Severidad.choices,
        default=Severidad.MEDIO,
    )
    descripcion = models.TextField(null=True, blank=True)
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)
    fecha_evento = models.DateTimeField(default=timezone.now)
    atendido = models.BooleanField(default=False)
    fecha_atencion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'auditoria_seguridad'
        ordering = ['-fecha_evento']
        indexes = [
            models.Index(fields=['nivel_severidad', '-fecha_evento'], name='ix_auditoria_seguridad_fecha'),
        ]
