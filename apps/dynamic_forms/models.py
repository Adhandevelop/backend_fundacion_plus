import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class Formulario(models.Model):
    """
    Tabla SQL: plus.formularios
    Definición raíz de un formulario dinámico institucional.
    """

    class Estado(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        PUBLICADO = 'publicado', 'Publicado'
        CERRADO = 'cerrado', 'Cerrado'
        ARCHIVADO = 'archivado', 'Archivado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, default='')
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.BORRADOR,
        db_index=True,
    )
    requiere_documento = models.BooleanField(default=False)
    permite_multiples_envios = models.BooleanField(default=True)
    numero_version_publicada = models.PositiveIntegerField(
        default=0,
        help_text='Última versión formal congelada y publicada (0 si solo tiene borrador)',
    )
    revision_edicion = models.PositiveIntegerField(
        default=0,
        help_text='Contador incremental de edición para concurrencia optimista',
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='formularios_creados',
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'formularios'
        ordering = ['-fecha_creacion']

    def save(self, *args, **kwargs):
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.titulo} [{self.estado} - v{self.numero_version_publicada}.r{self.revision_edicion}]'


class FormularioVersion(models.Model):
    """
    Tabla SQL: plus.formulario_versiones
    Versión formal inmutable y congelada de un formulario publicado.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    formulario = models.ForeignKey(
        Formulario,
        on_delete=models.CASCADE,
        related_name='versiones',
    )
    numero_version = models.PositiveIntegerField()
    es_vigente = models.BooleanField(default=True, db_index=True)
    titulo_congelado = models.CharField(max_length=255)
    descripcion_congelada = models.TextField(blank=True, default='')
    requiere_documento = models.BooleanField(default=False)
    permite_multiples_envios = models.BooleanField(default=True)
    publicado_en = models.DateTimeField(default=timezone.now)
    publicado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'formulario_versiones'
        ordering = ['formulario', '-numero_version']
        unique_together = [('formulario', 'numero_version')]

    def __str__(self):
        return f'{self.formulario.slug} (v{self.numero_version})'


class FormularioPregunta(models.Model):
    """
    Tabla SQL: plus.formulario_preguntas
    Pregunta perteneciente a una versión congelada o al borrador de trabajo del formulario.
    """

    class TipoCampo(models.TextChoices):
        TEXTO_CORTO = 'texto_corto', 'Texto Corto'
        TEXTO_LARGO = 'texto_largo', 'Texto Largo'
        NUMERO = 'numero', 'Número'
        FECHA = 'fecha', 'Fecha (YYYY-MM-DD)'
        BOOLEANO = 'booleano', 'Booleano (Sí/No)'
        SELECCION_UNICA = 'seleccion_unica', 'Selección Única'
        SELECCION_MULTIPLE = 'seleccion_multiple', 'Selección Múltiple'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.ForeignKey(
        FormularioVersion,
        on_delete=models.CASCADE,
        related_name='preguntas',
        null=True,
        blank=True,
    )
    formulario_borrador = models.ForeignKey(
        Formulario,
        on_delete=models.CASCADE,
        related_name='preguntas_borrador',
        null=True,
        blank=True,
    )
    codigo = models.CharField(max_length=60)
    enunciado = models.TextField()
    descripcion_ayuda = models.TextField(blank=True, default='')
    tipo_campo = models.CharField(max_length=30, choices=TipoCampo.choices)
    es_obligatorio = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=1)
    configuracion_validacion = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'formulario_preguntas'
        ordering = ['orden', 'codigo']

    def __str__(self):
        return f'[{self.codigo}] {self.enunciado[:50]}'


class FormularioOpcion(models.Model):
    """
    Tabla SQL: plus.formulario_opciones
    Opción admisible para preguntas de selección única o múltiple.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pregunta = models.ForeignKey(
        FormularioPregunta,
        on_delete=models.CASCADE,
        related_name='opciones',
    )
    valor = models.CharField(max_length=100)
    etiqueta = models.CharField(max_length=255)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'formulario_opciones'
        ordering = ['orden', 'valor']

    def __str__(self):
        return f'{self.etiqueta} ({self.valor})'


class FormularioEnvio(models.Model):
    """
    Tabla SQL: plus.formulario_envios
    Registro inmutable de un envío público o autenticado de un formulario.
    """

    class EstadoVinculacion(models.TextChoices):
        VINCULADO = 'vinculado', 'Vinculado a Cuenta'
        PENDIENTE_ACTIVACION = 'pendiente_activacion', 'Pendiente de Activación de Cuenta'
        PENDIENTE_REIVINDICACION = 'pendiente_reivindicacion', 'Pendiente de Reivindicación de Envío'
        CONFLICTO_IDENTIDAD = 'conflicto_identidad', 'Conflicto de Identidad'
        PENDIENTE_VERIFICACION = 'pendiente_verificacion', 'Pendiente de Verificación de Identidad'
        CONTACTO_INSTITUCIONAL = 'contacto_institucional', 'Contacto Institucional'
        RECHAZADO_POR_POLITICA = 'rechazado_por_politica', 'Rechazado por Política de Cuenta'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    formulario = models.ForeignKey(
        Formulario,
        on_delete=models.CASCADE,
        related_name='envios',
    )
    version = models.ForeignKey(
        FormularioVersion,
        on_delete=models.PROTECT,
        related_name='envios',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='formulario_envios',
    )
    estado_vinculacion = models.CharField(
        max_length=35,
        choices=EstadoVinculacion.choices,
        default=EstadoVinculacion.PENDIENTE_ACTIVACION,
        db_index=True,
    )
    nombres_declarados = models.CharField(max_length=150)
    apellidos_declarados = models.CharField(max_length=150)
    correo_declarado = models.EmailField(max_length=254, db_index=True)
    telefono_declarado = models.CharField(max_length=30, blank=True, default='')
    tipo_documento_declarado = models.CharField(max_length=20, blank=True, default='')
    numero_documento_declarado = models.CharField(max_length=50, blank=True, default='')

    aceptacion_legal = models.ForeignKey(
        'communications.LegalAcceptance',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='formulario_envios',
    )
    ip_origen = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')

    idempotency_key = models.UUIDField(null=True, blank=True, db_index=True)
    idempotency_hash = models.CharField(max_length=64, blank=True, default='', db_index=True)
    fecha_envio = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'formulario_envios'
        ordering = ['-fecha_envio']
        indexes = [
            models.Index(fields=['formulario', '-fecha_envio']),
            models.Index(fields=['correo_declarado', 'estado_vinculacion']),
        ]

    def __str__(self):
        return f'Envío {self.id} en {self.formulario.slug} ({self.estado_vinculacion})'


class FormularioRespuesta(models.Model):
    """
    Tabla SQL: plus.formulario_respuestas
    Valor tipado inmutable registrado para cada pregunta respondida en un envío.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    envio = models.ForeignKey(
        FormularioEnvio,
        on_delete=models.CASCADE,
        related_name='respuestas',
    )
    pregunta = models.ForeignKey(
        FormularioPregunta,
        on_delete=models.PROTECT,
        related_name='respuestas',
    )
    codigo_pregunta = models.CharField(max_length=60)
    enunciado_congelado = models.TextField(blank=True, default='')
    tipo_campo_congelado = models.CharField(max_length=30, blank=True, default='')
    valor_texto = models.TextField(null=True, blank=True)
    valor_numero = models.DecimalField(max_digits=16, decimal_places=4, null=True, blank=True)
    valor_fecha = models.DateField(null=True, blank=True)
    valor_booleano = models.BooleanField(null=True, blank=True)
    valores_seleccionados = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'formulario_respuestas'
        ordering = ['pregunta__orden', 'codigo_pregunta']

    def __str__(self):
        return f'Respuesta a {self.codigo_pregunta} en envío {self.envio_id}'


class FormularioToken(models.Model):
    """
    Tabla SQL: plus.formulario_tokens
    Tokens seguros de un solo uso con hash SHA-256 para activación de cuenta o confirmación de envío.
    """

    class Proposito(models.TextChoices):
        ACTIVAR_CUENTA = 'activar_cuenta', 'Activar Cuenta Ciudadana'
        REIVINDICAR_ENVIO = 'reivindicar_envio', 'Reivindicar Envío Existente'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='formulario_tokens',
        null=True,
        blank=True,
    )
    correo = models.EmailField(max_length=254, db_index=True)
    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    proposito = models.CharField(max_length=30, choices=Proposito.choices)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_expiracion = models.DateTimeField(db_index=True)
    usado = models.BooleanField(default=False, db_index=True)
    fecha_uso = models.DateTimeField(null=True, blank=True)
    ip_creacion = models.GenericIPAddressField(null=True, blank=True)
    ip_uso = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'formulario_tokens'
        ordering = ['-fecha_creacion']

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.fecha_expiracion

    def __str__(self):
        return f'Token {self.proposito} para {self.correo} (Usado: {self.usado})'


class FormularioNotificacion(models.Model):
    """
    Tabla SQL: plus.formulario_notificaciones
    Registro desacoplado de las tareas y estado de despacho de correos informativos o de activación.
    """

    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        ENVIADO = 'enviado', 'Enviado'
        FALLIDO = 'fallido', 'Fallido'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    envio = models.ForeignKey(
        FormularioEnvio,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        null=True,
        blank=True,
    )
    correo_destino = models.EmailField(max_length=254)
    asunto = models.CharField(max_length=255)
    cuerpo_texto = models.TextField(blank=True, default='')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    error_mensaje = models.TextField(blank=True, default='')
    intentos = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_envio = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'formulario_notificaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Notificación a {self.correo_destino} [{self.estado}]'
