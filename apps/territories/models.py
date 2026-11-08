import uuid
from django.core.validators import RegexValidator
from django.db import models
from core.gis import PostGISMultiPolygonField


class Department(models.Model):
    """
    Tabla SQL: plus.departamentos
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_departamento',
    )
    codigo_dane = models.CharField(
        max_length=2,
        unique=True,
        validators=[RegexValidator(r'^[0-9]{2}$', 'El código DANE departamental debe tener 2 dígitos.')],
    )
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'departamentos'
        ordering = ['nombre']

    @property
    def id_departamento(self):
        return self.id

    def __str__(self):
        return f'{self.nombre} ({self.codigo_dane})'


class Municipality(models.Model):
    """
    Tabla SQL: plus.municipios
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_municipio',
    )
    departamento = models.ForeignKey(
        Department,
        on_delete=models.RESTRICT,
        db_column='id_departamento',
        related_name='municipios',
    )
    codigo_dane = models.CharField(
        max_length=5,
        unique=True,
        validators=[RegexValidator(r'^[0-9]{5}$', 'El código DANE municipal debe tener 5 dígitos.')],
    )
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'municipios'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['departamento'], name='ix_municipios_departamento'),
        ]

    @property
    def id_municipio(self):
        return self.id

    def __str__(self):
        return f'{self.nombre} ({self.codigo_dane})'


class Community(models.Model):
    """
    Tabla SQL: plus.comunidades
    """

    class TipoComunidad(models.TextChoices):
        BARRIO = 'barrio', 'Barrio'
        VEREDA = 'vereda', 'Vereda'
        CORREGIMIENTO = 'corregimiento', 'Corregimiento'
        COMUNA = 'comuna', 'Comuna'
        SECTOR = 'sector', 'Sector'
        OTRO = 'otro', 'Otro'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_comunidad',
    )
    municipio = models.ForeignKey(
        Municipality,
        on_delete=models.RESTRICT,
        db_column='id_municipio',
        related_name='comunidades',
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)
    tipo = models.CharField(
        max_length=50,
        choices=TipoComunidad.choices,
        default=TipoComunidad.VEREDA,
    )
    ubicacion = PostGISMultiPolygonField(
        null=True,
        blank=True,
        db_column='ubicacion',
        help_text='Perímetro opcional geometry(MultiPolygon, 4326)',
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'comunidades'
        ordering = ['municipio__nombre', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['municipio', 'tipo', 'nombre'],
                name='uq_comunidad_territorio',
            ),
        ]
        indexes = [
            models.Index(fields=['municipio'], name='ix_comunidades_municipio'),
        ]

    @property
    def id_comunidad(self):
        return self.id

    def __str__(self):
        return f'{self.nombre} ({self.tipo} - {self.municipio.nombre})'
