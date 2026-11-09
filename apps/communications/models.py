import hashlib
import secrets
import uuid
from datetime import timedelta
from django.conf import settings
from django.db import models
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


class LegalDocument(models.Model):
    """
    Tabla SQL (AMP-09): plus.documentos_legales
    Versionado de políticas de tratamiento de datos, términos de uso y avisos legales.
    """

    class Tipo(models.TextChoices):
        TRATAMIENTO_DATOS = 'tratamiento_datos', 'Política de tratamiento de datos personales'
        TERMINOS_USO = 'terminos_uso', 'Términos y condiciones de uso'
        RADICACION_CASO = 'radicacion_caso', 'Declaración de veracidad y radicación'
        BOLETIN = 'boletin', 'Consentimiento de suscripción a boletín'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_documento',
    )
    tipo = models.CharField(max_length=50, choices=Tipo.choices, default=Tipo.TRATAMIENTO_DATOS)
    version = models.CharField(max_length=30, default='1.0')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    vigente = models.BooleanField(default=True)
    fecha_vigencia = models.DateTimeField(default=timezone.now)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'documentos_legales'
        ordering = ['tipo', '-fecha_vigencia']
        constraints = [
            models.UniqueConstraint(fields=['tipo', 'version'], name='uq_documento_legal_version'),
        ]

    @classmethod
    def get_current(cls, tipo: str = 'tratamiento_datos'):
        doc = cls.objects.filter(tipo=tipo, vigente=True).order_by('-fecha_vigencia').first()
        if not doc:
            doc, _ = cls.objects.get_or_create(
                tipo=tipo,
                version='1.0',
                defaults={
                    'titulo': dict(cls.Tipo.choices).get(tipo, 'Política de Tratamiento de Datos PLUS'),
                    'contenido': (
                        'Autorización de tratamiento de datos personales conforme a la Ley 1581 de 2012 '
                        'y lineamientos institucionales de la Corporación Pluralismo Social (PLUS).'
                    ),
                    'vigente': True,
                },
            )
        return doc

    def __str__(self):
        return f'{self.tipo} v{self.version}'


class LegalAcceptance(models.Model):
    """
    Tabla SQL (AMP-09): plus.aceptaciones_legales
    Trazabilidad inmutable de consentimientos otorgados en registro, casos, propuestas y boletín.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_aceptacion',
    )
    documento = models.ForeignKey(
        LegalDocument,
        on_delete=models.RESTRICT,
        db_column='id_documento',
        related_name='aceptaciones',
    )
    version_aceptada = models.CharField(max_length=30)
    finalidad = models.CharField(max_length=50)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='aceptaciones_legales',
    )
    caso = models.ForeignKey(
        'cases.Case',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_caso',
        related_name='aceptaciones_legales',
    )
    propuesta = models.ForeignKey(
        EventProposal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_propuesta',
        related_name='aceptaciones_legales',
    )
    correo_declarado = models.EmailField(max_length=150, null=True, blank=True)
    fecha_aceptacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'aceptaciones_legales'
        ordering = ['-fecha_aceptacion']

    @classmethod
    def record(
        cls,
        *,
        finalidad: str,
        tipo_documento: str = 'tratamiento_datos',
        version: str | None = None,
        usuario=None,
        caso=None,
        propuesta=None,
        correo_declarado: str | None = None,
    ):
        doc = LegalDocument.get_current(tipo_documento)
        return cls.objects.create(
            documento=doc,
            version_aceptada=version or doc.version,
            finalidad=finalidad,
            usuario=usuario if (usuario and getattr(usuario, 'is_authenticated', True)) else None,
            caso=caso,
            propuesta=propuesta,
            correo_declarado=correo_declarado or (getattr(usuario, 'correo', None) if usuario else None),
        )

    def __str__(self):
        return f'Aceptación {self.finalidad} ({self.version_aceptada})'


class NewsletterSubscription(models.Model):
    """
    Tabla SQL (AMP-02): plus.suscripciones_boletin
    """

    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente de confirmación'
        CONFIRMADA = 'confirmada', 'Confirmada'
        BAJA = 'baja', 'Dada de baja'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_suscripcion',
    )
    nombre = models.CharField(max_length=150, null=True, blank=True)
    correo = models.EmailField(max_length=150, unique=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='suscripciones_boletin',
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    token_hash = models.CharField(max_length=128, null=True, blank=True)
    expira_en = models.DateTimeField(null=True, blank=True)
    aceptacion_legal = models.ForeignKey(
        LegalAcceptance,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_aceptacion_legal',
        related_name='suscripciones_boletin',
    )
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'suscripciones_boletin'
        ordering = ['-fecha_solicitud']

    @staticmethod
    def hash_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode('utf-8')).hexdigest()

    def generate_token(self, hours: int = 48) -> str:
        raw = secrets.token_urlsafe(32)
        self.token_hash = self.hash_token(raw)
        self.expira_en = timezone.now() + timedelta(hours=hours)
        return raw

    def save(self, *args, **kwargs):
        self.correo = self.correo.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.correo} ({self.estado})'
