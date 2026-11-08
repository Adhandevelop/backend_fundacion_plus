import uuid
from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class CaseComment(models.Model):
    """
    Tabla SQL: plus.comentarios
    """

    class EstadoModeracion(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        APROBADO = 'aprobado', 'Aprobado'
        RECHAZADO = 'rechazado', 'Rechazado'
        OCULTO = 'oculto', 'Oculto'

    ModerationStatus = EstadoModeracion

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_comentario',
    )
    caso = models.ForeignKey(
        'cases.Case',
        on_delete=models.RESTRICT,
        db_column='id_caso',
        related_name='comentarios',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_usuario',
        related_name='comentarios',
    )
    contenido = models.TextField()
    estado_moderacion = models.CharField(
        max_length=20,
        choices=EstadoModeracion.choices,
        default=EstadoModeracion.PENDIENTE,
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'comentarios'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(
                fields=['caso', 'estado_moderacion', '-fecha_creacion'],
                name='ix_comentarios_caso',
            ),
            models.Index(fields=['usuario'], name='ix_comentarios_usuario'),
        ]

    @property
    def id_comentario(self):
        return self.id

    def __str__(self):
        return f'Comentario en {self.caso.codigo} ({self.estado_moderacion})'


class CaseMessage(models.Model):
    """
    Tabla SQL: plus.mensajes_privados
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_mensaje',
    )
    caso = models.ForeignKey(
        'cases.Case',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_caso',
        related_name='mensajes_privados',
    )
    remitente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_remitente',
        related_name='mensajes_enviados',
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_destinatario',
        related_name='mensajes_recibidos',
    )
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'mensajes_privados'
        ordering = ['fecha_envio']
        constraints = [
            models.CheckConstraint(
                check=~Q(remitente=F('destinatario')),
                name='ck_mensaje_destino',
            ),
            models.CheckConstraint(
                check=Q(fecha_lectura__isnull=True) | Q(fecha_lectura__gte=F('fecha_envio')),
                name='ck_fecha_lectura',
            ),
        ]
        indexes = [
            models.Index(fields=['destinatario', '-fecha_envio'], name='ix_mensajes_destinatario'),
            models.Index(fields=['remitente', '-fecha_envio'], name='ix_mensajes_remitente'),
            models.Index(fields=['caso'], name='ix_mensajes_caso'),
        ]

    @property
    def id_mensaje(self):
        return self.id

    def __str__(self):
        return f'Mensaje privado ({self.remitente.correo} -> {self.destinatario.correo})'


class EventProposal(models.Model):
    """
    Tabla SQL: plus.propuestas_iniciativas
    """

    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        EN_REVISION = 'en_revision', 'En Revisión'
        APROBADA = 'aprobada', 'Aprobada'
        RECHAZADA = 'rechazada', 'Rechazada'

    Status = Estado

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_propuesta',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='propuestas_iniciativas',
    )
    comunidad = models.ForeignKey(
        'territories.Community',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_comunidad',
        related_name='propuestas_iniciativas',
    )
    nombre_contacto = models.CharField(max_length=150, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=25, null=True, blank=True)
    comunidad_declarada = models.CharField(max_length=200, null=True, blank=True)
    acepta_tratamiento_datos = models.BooleanField(default=False)
    iniciativa_solicitada = models.ForeignKey(
        'initiatives.Initiative',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_iniciativa_solicitada',
        related_name='propuestas_solicitadas',
    )
    iniciativa_generada = models.ForeignKey(
        'initiatives.Initiative',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_iniciativa_generada',
        related_name='propuestas_origen',
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_actividad = models.CharField(max_length=80, null=True, blank=True)
    fecha_sugerida = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    respuesta = models.TextField(null=True, blank=True)
    revisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_revisor',
        related_name='propuestas_revisadas',
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_revision = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'propuestas_iniciativas'
        ordering = ['-fecha_creacion']
        constraints = [
            models.CheckConstraint(
                check=Q(acepta_tratamiento_datos=True),
                name='ck_propuesta_consentimiento',
            ),
            models.CheckConstraint(
                check=Q(comunidad__isnull=False) | Q(comunidad_declarada__isnull=False),
                name='ck_propuesta_territorio',
            ),
            models.CheckConstraint(
                check=Q(usuario__isnull=False) | (Q(nombre_contacto__isnull=False) & Q(telefono_contacto__isnull=False)),
                name='ck_propuesta_contacto',
            ),
        ]
        indexes = [
            models.Index(fields=['usuario', '-fecha_creacion'], name='ix_propuestas_usuario'),
            models.Index(fields=['comunidad', 'estado'], name='ix_propuestas_comunidad_estado'),
        ]

    @property
    def id_propuesta(self):
        return self.id

    def __str__(self):
        return f'Propuesta: {self.titulo} ({self.estado})'


class SiteSetting(models.Model):
    """
    Tabla SQL: plus.configuracion_plataforma
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_configuracion',
    )
    clave = models.CharField(max_length=100, unique=True)
    valor = models.JSONField(default=dict)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'configuracion_plataforma'
        ordering = ['clave']

    @property
    def id_configuracion(self):
        return self.id

    @property
    def key(self):
        return self.clave

    @property
    def value(self):
        return self.valor

    def save(self, *args, **kwargs):
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.clave
