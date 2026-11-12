import uuid
from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from django.utils.text import slugify
from core.gis import PostGISPointField


class Initiative(models.Model):
    """
    Tabla SQL: plus.iniciativas
    """

    class Estado(models.TextChoices):
        PLANIFICADA = 'planificada', 'Planificada'
        EN_CURSO = 'en_curso', 'En Curso'
        FINALIZADA = 'finalizada', 'Finalizada'
        CANCELADA = 'cancelada', 'Cancelada'

    class EstadoPublicacion(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        PENDIENTE = 'pendiente', 'Pendiente'
        PUBLICADA = 'publicada', 'Publicada'
        RECHAZADA = 'rechazada', 'Rechazada'

    PublicationStatus = EstadoPublicacion

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_iniciativa',
    )
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_creador',
        related_name='iniciativas_creadas',
    )
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    descripcion_corta = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    categoria = models.CharField(max_length=80)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PLANIFICADA,
    )
    estado_publicacion = models.CharField(
        max_length=20,
        choices=EstadoPublicacion.choices,
        default=EstadoPublicacion.BORRADOR,
    )
    destacada = models.BooleanField(default=False)
    orden_destacado = models.IntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'iniciativas'
        ordering = ['orden_destacado', '-fecha_publicacion', '-fecha_creacion']
        indexes = [
            models.Index(fields=['categoria', 'estado_publicacion'], name='ix_iniciativas_categoria'),
        ]

    @property
    def id_iniciativa(self):
        return self.id

    @property
    def name(self):
        return self.titulo

    def get_or_create_current_edition(self):
        current_year = timezone.now().year
        edicion, _ = self.ediciones.get_or_create(
            anio=current_year,
            defaults={'nombre_edicion': f'{self.titulo} {current_year}'},
        )
        return edicion

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo) or 'iniciativa'
            slug = base_slug
            counter = 1
            while Initiative.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        if self.estado_publicacion == self.EstadoPublicacion.PUBLICADA and not self.fecha_publicacion:
            self.fecha_publicacion = timezone.now()
        if self.destacada and self.estado_publicacion != self.EstadoPublicacion.PUBLICADA:
            self.destacada = False
            self.orden_destacado = None
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class InitiativeEdition(models.Model):
    """
    Tabla SQL: plus.iniciativa_ediciones
    """

    class Estado(models.TextChoices):
        PLANIFICADA = 'planificada', 'Planificada'
        EN_CURSO = 'en_curso', 'En Curso'
        FINALIZADA = 'finalizada', 'Finalizada'
        CANCELADA = 'cancelada', 'Cancelada'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_edicion',
    )
    iniciativa = models.ForeignKey(
        Initiative,
        on_delete=models.RESTRICT,
        db_column='id_iniciativa',
        related_name='ediciones',
    )
    anio = models.SmallIntegerField()
    nombre_edicion = models.CharField(max_length=150, null=True, blank=True)
    temporada = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PLANIFICADA,
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'iniciativa_ediciones'
        ordering = ['-anio', '-fecha_creacion']
        constraints = [
            models.UniqueConstraint(fields=['iniciativa', 'anio'], name='uq_edicion_anual'),
            models.UniqueConstraint(fields=['iniciativa', 'id'], name='uq_edicion_pertenencia'),
        ]
        indexes = [
            models.Index(fields=['iniciativa', '-anio'], name='ix_ediciones_iniciativa_anio'),
        ]

    @property
    def id_edicion(self):
        return self.id

    def __str__(self):
        return f'{self.iniciativa.titulo} ({self.anio})'


class InitiativeMedia(models.Model):
    """
    Tabla SQL: plus.iniciativa_multimedia
    """

    class Tipo(models.TextChoices):
        IMAGEN = 'imagen', 'Imagen'
        VIDEO = 'video', 'Video'
        DOCUMENTO = 'documento', 'Documento'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_multimedia',
    )
    iniciativa = models.ForeignKey(
        Initiative,
        on_delete=models.RESTRICT,
        db_column='id_iniciativa',
        related_name='multimedia',
    )
    edicion = models.ForeignKey(
        InitiativeEdition,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_edicion',
        related_name='multimedia',
    )
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.IMAGEN,
    )
    ruta_archivo = models.TextField()
    texto_alternativo = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    es_portada = models.BooleanField(default=False)
    orden = models.IntegerField(default=0)
    fecha_subida = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'iniciativa_multimedia'
        ordering = ['orden', '-fecha_subida']
        indexes = [
            models.Index(fields=['iniciativa', 'orden'], name='ix_multimedia_iniciativa'),
            models.Index(fields=['edicion', 'orden'], name='ix_multimedia_edicion'),
        ]

    @property
    def id_multimedia(self):
        return self.id

    def __str__(self):
        return f'Multimedia {self.tipo} ({self.iniciativa.titulo})'


class InitiativeMetric(models.Model):
    """
    Tabla SQL: plus.iniciativa_indicadores
    """

    class TipoMedicion(models.TextChoices):
        ESTIMADO = 'estimado', 'Estimado'
        REAL = 'real', 'Real'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_indicador',
    )
    edicion = models.ForeignKey(
        InitiativeEdition,
        on_delete=models.RESTRICT,
        db_column='id_edicion',
        related_name='indicadores',
    )
    nombre = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    unidad = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    icono = models.CharField(max_length=50, null=True, blank=True)
    tipo_medicion = models.CharField(
        max_length=20,
        choices=TipoMedicion.choices,
        default=TipoMedicion.REAL,
    )
    orden = models.IntegerField(default=0)
    fecha_corte = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'iniciativa_indicadores'
        ordering = ['orden', 'nombre']
        indexes = [
            models.Index(fields=['edicion', 'orden'], name='ix_indicadores_edicion'),
        ]

    @property
    def id_indicador(self):
        return self.id

    def __str__(self):
        return f'{self.nombre}: {self.valor}'


class InitiativeCommunity(models.Model):
    """
    Tabla SQL: plus.iniciativa_comunidades
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_iniciativa_comunidad',
    )
    edicion = models.ForeignKey(
        InitiativeEdition,
        on_delete=models.RESTRICT,
        db_column='id_edicion',
        related_name='comunidades_vinculadas',
    )
    comunidad = models.ForeignKey(
        'territories.Community',
        on_delete=models.RESTRICT,
        db_column='id_comunidad',
        related_name='ediciones_iniciativas',
    )
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'iniciativa_comunidades'
        constraints = [
            models.UniqueConstraint(fields=['edicion', 'comunidad'], name='uq_edicion_comunidad'),
        ]
        indexes = [
            models.Index(fields=['comunidad'], name='ix_iniciativa_comunidades_com'),
        ]

    def __str__(self):
        return f'{self.edicion} - {self.comunidad.nombre}'


class InitiativeActivity(models.Model):
    """
    Tabla SQL: plus.iniciativa_actividades
    """

    class Estado(models.TextChoices):
        PROGRAMADA = 'programada', 'Programada'
        REALIZADA = 'realizada', 'Realizada'
        CANCELADA = 'cancelada', 'Cancelada'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_actividad',
    )
    edicion = models.ForeignKey(
        InitiativeEdition,
        on_delete=models.RESTRICT,
        db_column='id_edicion',
        related_name='actividades',
    )
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_responsable',
        related_name='actividades_iniciativa',
    )
    comunidad = models.ForeignKey(
        'territories.Community',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='id_comunidad',
        related_name='actividades_iniciativa',
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    lugar = models.CharField(max_length=200, null=True, blank=True)
    ubicacion = PostGISPointField(
        null=True,
        blank=True,
        db_column='ubicacion',
        help_text='Coordenada geográfica PostGIS geometry(Point, 4326)',
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PROGRAMADA,
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'iniciativa_actividades'
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['edicion', 'fecha_inicio'], name='ix_actividades_edicion_fecha'),
            models.Index(fields=['comunidad'], name='ix_actividades_comunidad'),
            models.Index(fields=['responsable'], name='ix_actividades_responsable'),
        ]

    @property
    def id_actividad(self):
        return self.id

    def __str__(self):
        return f'{self.titulo} ({self.edicion})'


class InitiativeCaseLink(models.Model):
    """
    Tabla SQL: plus.iniciativa_casos
    Vincula ediciones de iniciativas con casos comunitarios (hallazgo, seguimiento, resultado, otro).
    """

    class TipoVinculo(models.TextChoices):
        HALLAZGO = 'hallazgo', 'Hallazgo'
        SEGUIMIENTO = 'seguimiento', 'Seguimiento'
        RESULTADO = 'resultado', 'Resultado'
        OTRO = 'otro', 'Otro'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_iniciativa_caso',
    )
    edicion = models.ForeignKey(
        InitiativeEdition,
        on_delete=models.RESTRICT,
        db_column='id_edicion',
        related_name='casos_vinculados',
    )
    caso = models.ForeignKey(
        'cases.Case',
        on_delete=models.RESTRICT,
        db_column='id_caso',
        related_name='iniciativas_vinculadas',
    )
    tipo_vinculo = models.CharField(
        max_length=30,
        choices=TipoVinculo.choices,
        default=TipoVinculo.HALLAZGO,
    )
    observaciones = models.TextField(null=True, blank=True)
    fecha_vinculacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'iniciativa_casos'
        ordering = ['-fecha_vinculacion']
        constraints = [
            models.UniqueConstraint(fields=['edicion', 'caso'], name='uq_edicion_caso'),
        ]
        indexes = [
            models.Index(fields=['caso'], name='ix_iniciativa_casos_caso'),
        ]

    def __str__(self):
        return f'{self.edicion} <-> {self.caso.codigo} ({self.tipo_vinculo})'
