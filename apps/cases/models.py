import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models, transaction
from django.db.models import F, Q
from django.utils import timezone
from core.gis import PostGISPointField, make_geojson_point, obfuscate_coordinates


class CaseCategory(models.Model):
    """
    Tabla SQL: plus.tipos_caso (Ampliada con AMP-12: naturaleza)
    """

    class Naturaleza(models.TextChoices):
        PROBLEMATICA = 'problematica', 'Problemática'
        PROYECTO_INICIATIVA = 'proyecto_iniciativa', 'Proyecto / Iniciativa'
        OTRO = 'otro', 'Otro'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_tipo_caso',
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    categoria = models.CharField(max_length=50, default='general')
    naturaleza = models.CharField(
        max_length=30,
        choices=Naturaleza.choices,
        default=Naturaleza.PROBLEMATICA,
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipos_caso'
        ordering = ['categoria', 'nombre']
        constraints = [
            models.UniqueConstraint(fields=['categoria', 'nombre'], name='uq_tipo_caso'),
        ]

    @property
    def id_tipo_caso(self):
        return self.id

    def __str__(self):
        return f'{self.nombre} ({self.categoria})'


class CaseStatus(models.Model):
    """
    Tabla SQL: plus.estados_caso
    Catálogo oficial en base de datos.md:
    1: 'pendiente', 2: 'en_revision', 3: 'en_proceso', 4: 'resuelto', 5: 'cerrado'
    """

    class Nombre(models.TextChoices):
        PENDIENTE = 'pendiente', 'Caso recibido pendiente de gestión'
        EN_REVISION = 'en_revision', 'Caso en verificación'
        EN_PROCESO = 'en_proceso', 'Caso en seguimiento'
        RESUELTO = 'resuelto', 'Caso solucionado'
        CERRADO = 'cerrado', 'Caso archivado o cerrado'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_estado',
    )
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    orden = models.IntegerField(unique=True)

    class Meta:
        db_table = 'estados_caso'
        ordering = ['orden']

    @property
    def id_estado(self):
        return self.id

    @classmethod
    def get_default_status(cls):
        obj, _ = cls.objects.get_or_create(
            nombre=cls.Nombre.PENDIENTE,
            defaults={'descripcion': 'Caso recibido pendiente de gestión', 'orden': 1},
        )
        return obj

    @classmethod
    def get_by_name(cls, name: str):
        name_map = {
            'RECEIVED': cls.Nombre.PENDIENTE,
            'PENDIENTE': cls.Nombre.PENDIENTE,
            'ASSIGNED': cls.Nombre.EN_REVISION,
            'EN_REVISION': cls.Nombre.EN_REVISION,
            'IN_PROGRESS': cls.Nombre.EN_PROCESO,
            'EN_PROCESO': cls.Nombre.EN_PROCESO,
            'RESOLVED': cls.Nombre.RESUELTO,
            'RESUELTO': cls.Nombre.RESUELTO,
            'CLOSED': cls.Nombre.CERRADO,
            'CERRADO': cls.Nombre.CERRADO,
        }
        order_map = {
            cls.Nombre.PENDIENTE: 1,
            cls.Nombre.EN_REVISION: 2,
            cls.Nombre.EN_PROCESO: 3,
            cls.Nombre.RESUELTO: 4,
            cls.Nombre.CERRADO: 5,
        }
        resolved = name_map.get(str(name).strip().upper(), str(name).strip().lower())
        obj, _ = cls.objects.get_or_create(
            nombre=resolved,
            defaults={
                'descripcion': dict(cls.Nombre.choices).get(resolved, resolved),
                'orden': order_map.get(resolved, cls.objects.count() + 10),
            },
        )
        return obj

    def __str__(self):
        return self.nombre


class Case(models.Model):
    """
    Tabla SQL: plus.casos (Ampliada con AMP-05 y AMP-11)
    """

    class Prioridad(models.TextChoices):
        BAJA = 'baja', 'Baja'
        MEDIA = 'media', 'Media'
        ALTA = 'alta', 'Alta'
        CRITICA = 'critica', 'Crítica'

    class EstadoPublicacion(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        APROBADO = 'aprobado', 'Aprobado'
        RECHAZADO = 'rechazado', 'Rechazado'

    # Aliases para compatibilidad con controladores y vistas
    Priority = Prioridad
    ModerationStatus = EstadoPublicacion
    ManagementStatus = CaseStatus.Nombre

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_caso',
    )
    codigo = models.CharField(max_length=30, unique=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_usuario',
        related_name='casos_reportados',
    )
    tipo_caso = models.ForeignKey(
        CaseCategory,
        on_delete=models.RESTRICT,
        db_column='id_tipo_caso',
        related_name='casos',
    )
    comunidad = models.ForeignKey(
        'territories.Community',
        on_delete=models.RESTRICT,
        db_column='id_comunidad',
        related_name='casos',
    )
    estado = models.ForeignKey(
        CaseStatus,
        on_delete=models.RESTRICT,
        db_column='id_estado',
        related_name='casos',
    )
    prioridad = models.CharField(
        max_length=20,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA,
    )
    estado_publicacion = models.CharField(
        max_length=20,
        choices=EstadoPublicacion.choices,
        default=EstadoPublicacion.PENDIENTE,
    )
    ubicacion = PostGISPointField(
        null=True,
        blank=True,
        db_column='ubicacion',
        help_text='Coordenada geográfica PostGIS geometry(Point, 4326)',
    )
    direccion_referencia = models.TextField(null=True, blank=True)

    # AMP-05: Cantidades de afectación (NULL = desconocido, >= 0 = valor reportado)
    familias_afectadas = models.PositiveIntegerField(null=True, blank=True)
    meses_afectacion = models.PositiveIntegerField(null=True, blank=True)

    # AMP-11: Resolución narrativa y trazabilidad del resultado vigente
    resultado_resumen = models.TextField(null=True, blank=True)
    seguimiento_resolucion = models.ForeignKey(
        'tracking.CaseUpdate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_seguimiento_resolucion',
        related_name='casos_resueltos',
    )
    usuario_resolucion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario_resolucion',
        related_name='casos_resueltos',
    )
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'casos'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['comunidad', 'estado'], name='ix_casos_comunidad_estado'),
            models.Index(fields=['tipo_caso'], name='ix_casos_tipo'),
            models.Index(fields=['usuario', '-fecha_creacion'], name='ix_casos_usuario_fecha'),
            models.Index(fields=['estado_publicacion', '-fecha_creacion'], name='ix_casos_estado_publicacion'),
        ]

    @classmethod
    def generate_codigo(cls) -> str:
        year = timezone.now().year
        prefix = f'PLUS-{year}-'
        with transaction.atomic():
            last_case = cls.objects.filter(codigo__startswith=prefix).order_by('-codigo').first()
            if last_case:
                try:
                    seq = int(last_case.codigo.split('-')[-1]) + 1
                except ValueError:
                    seq = cls.objects.filter(codigo__startswith=prefix).count() + 1
            else:
                seq = 1
            return f'{prefix}{seq:05d}'

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.generate_codigo()
        if not self.estado_id:
            self.estado = CaseStatus.get_default_status()
        if self.estado_publicacion == self.EstadoPublicacion.APROBADO and not self.fecha_aprobacion:
            self.fecha_aprobacion = timezone.now()
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    @property
    def id_caso(self):
        return self.id

    @property
    def radicado_code(self) -> str:
        return self.codigo

    @property
    def exact_longitude(self):
        if isinstance(self.ubicacion, dict) and self.ubicacion.get('coordinates'):
            return Decimal(str(self.ubicacion['coordinates'][0]))
        return None

    @property
    def exact_latitude(self):
        if isinstance(self.ubicacion, dict) and self.ubicacion.get('coordinates'):
            return Decimal(str(self.ubicacion['coordinates'][1]))
        return None

    @property
    def exact_location(self):
        return self.ubicacion

    @property
    def public_location(self):
        """
        Generaliza coordenadas exactas para proteger la privacidad ciudadana en vistas públicas
        (según requerimiento de seguridad en base de datos.md línea 60).
        """
        lat = self.exact_latitude
        lon = self.exact_longitude
        if lat is None or lon is None:
            return None
        gen_lat, gen_lon = obfuscate_coordinates(lat, lon)
        return make_geojson_point(gen_lon, gen_lat)

    @property
    def active_assignment(self):
        return self.asignaciones.filter(activo=True).select_related('responsable').first()

    @property
    def active_correction_request(self):
        return self.solicitudes_correccion.filter(
            estado=CaseCorrectionRequest.Estado.ABIERTA
        ).order_by('-fecha_solicitud').first()

    def __str__(self):
        return f'{self.codigo} - {self.titulo}'


class CaseAssignment(models.Model):
    """
    Tabla SQL: plus.asignaciones_casos
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_asignacion_caso',
    )
    caso = models.ForeignKey(
        Case,
        on_delete=models.RESTRICT,
        db_column='id_caso',
        related_name='asignaciones',
    )
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_responsable',
        related_name='casos_asignados',
    )
    asignador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_asignador',
        related_name='asignaciones_realizadas',
    )
    fecha_asignacion = models.DateTimeField(default=timezone.now)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'asignaciones_casos'
        ordering = ['-fecha_asignacion']
        constraints = [
            models.UniqueConstraint(
                fields=['caso'],
                condition=Q(activo=True),
                name='ux_asignacion_caso_activa',
            ),
        ]
        indexes = [
            models.Index(fields=['responsable'], name='ix_asignacion_caso_responsable'),
            models.Index(fields=['asignador'], name='ix_asignacion_caso_asignador'),
        ]

    @property
    def id_asignacion_caso(self):
        return self.id

    def __str__(self):
        return f'{self.caso.codigo} -> {self.responsable.correo}'


class CaseCorrectionRequest(models.Model):
    """
    Tabla SQL (AMP-06): plus.solicitudes_correccion
    Requerimientos formales de subsanación sobre un caso.
    """

    class Estado(models.TextChoices):
        ABIERTA = 'abierta', 'Abierta'
        RESPONDIDA = 'respondida', 'Respondida'
        CERRADA = 'cerrada', 'Cerrada'
        CANCELADA = 'cancelada', 'Cancelada'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_solicitud',
    )
    caso = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        db_column='id_caso',
        related_name='solicitudes_correccion',
    )
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_solicitante',
        related_name='solicitudes_correccion_creadas',
    )
    motivo = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ABIERTA,
    )
    respuesta = models.TextField(null=True, blank=True)
    revisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_revisor',
        related_name='solicitudes_correccion_revisadas',
    )
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'solicitudes_correccion'
        ordering = ['-fecha_solicitud']
        indexes = [
            models.Index(fields=['caso', 'estado'], name='ix_solicitudes_corr_caso'),
        ]

    def __str__(self):
        return f'Solicitud de corrección {self.estado} en {self.caso.codigo}'


class CaseContribution(models.Model):
    """
    Tabla SQL (AMP-07): plus.aportes_caso
    Aportes privados de información o respuesta del ciudadano al expediente.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_aporte',
    )
    caso = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        db_column='id_caso',
        related_name='aportes',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_usuario',
        related_name='aportes_caso',
    )
    solicitud_correccion = models.ForeignKey(
        CaseCorrectionRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_solicitud_correccion',
        related_name='aportes',
    )
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'aportes_caso'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['caso', '-fecha_creacion'], name='ix_aportes_caso_fecha'),
        ]

    def __str__(self):
        return f'Aporte en {self.caso.codigo} por {self.usuario.correo}'


class CaseEvidence(models.Model):
    """
    Tabla SQL: plus.evidencias (Ampliada con AMP-07 y AMP-10)
    """

    class TipoArchivo(models.TextChoices):
        IMAGEN = 'imagen', 'Imagen'
        VIDEO = 'video', 'Video'
        AUDIO = 'audio', 'Audio'
        DOCUMENTO = 'documento', 'Documento'

    class Audiencia(models.TextChoices):
        PUBLICO = 'publico', 'Público'
        CIUDADANO = 'ciudadano', 'Ciudadano / Equipo'
        PRIVADO = 'privado', 'Privado / Interno'

    class EstadoRevision(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        APROBADA = 'aprobada', 'Aprobada'
        RECHAZADA = 'rechazada', 'Rechazada'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_evidencia',
    )
    caso = models.ForeignKey(
        Case,
        on_delete=models.RESTRICT,
        db_column='id_caso',
        related_name='evidencias',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_usuario',
        related_name='evidencias_subidas',
    )
    aporte = models.ForeignKey(
        CaseContribution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_aporte',
        related_name='evidencias',
    )
    seguimiento = models.ForeignKey(
        'tracking.CaseUpdate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_seguimiento',
        related_name='evidencias',
    )
    tipo_archivo = models.CharField(
        max_length=30,
        choices=TipoArchivo.choices,
        default=TipoArchivo.IMAGEN,
    )
    ruta_archivo = models.TextField()
    descripcion = models.TextField(null=True, blank=True)

    # AMP-10: Visibilidad/audiencia individual, estado de revisión y metadatos de almacenamiento
    audiencia = models.CharField(
        max_length=20,
        choices=Audiencia.choices,
        default=Audiencia.CIUDADANO,
    )
    estado_revision = models.CharField(
        max_length=20,
        choices=EstadoRevision.choices,
        default=EstadoRevision.PENDIENTE,
    )
    nombre_original = models.CharField(max_length=255, null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    tamano_bytes = models.BigIntegerField(null=True, blank=True)

    fecha_subida = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'evidencias'
        ordering = ['-fecha_subida']
        indexes = [
            models.Index(fields=['caso'], name='ix_evidencias_caso'),
            models.Index(fields=['seguimiento'], name='ix_evidencias_seguimiento'),
        ]

    @property
    def id_evidencia(self):
        return self.id

    @property
    def id_seguimiento(self):
        return self.seguimiento_id

    def __str__(self):
        return f'Evidencia {self.tipo_archivo} en {self.caso.codigo}'


class FollowedCase(models.Model):
    """
    Tabla SQL (AMP-03): plus.casos_seguidos
    Relación usuario-caso para seguimiento de novedades públicas.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_seguimiento_usuario',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='casos_seguidos',
    )
    caso = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        db_column='id_caso',
        related_name='seguidores',
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'casos_seguidos'
        ordering = ['-fecha_creacion']
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'caso'], name='uq_usuario_caso_seguido'),
        ]

    def __str__(self):
        return f'{self.usuario.correo} sigue {self.caso.codigo}'
