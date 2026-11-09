import uuid
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify


class NewsCategory(models.Model):
    """
    Tabla SQL (AMP-01): plus.categorias_noticias
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_categoria_noticia',
    )
    nombre = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'categorias_noticias'
        ordering = ['nombre']

    def __init__(self, *args, **kwargs):
        if 'name' in kwargs and 'nombre' not in kwargs:
            kwargs['nombre'] = kwargs.pop('name')
        if 'description' in kwargs and 'descripcion' not in kwargs:
            kwargs['descripcion'] = kwargs.pop('description')
        if 'is_active' in kwargs and 'activa' not in kwargs:
            kwargs['activa'] = kwargs.pop('is_active')
        super().__init__(*args, **kwargs)

    @property
    def id_categoria_noticia(self):
        return self.id

    @property
    def name(self):
        return self.nombre

    @name.setter
    def name(self, val):
        self.nombre = val

    @property
    def description(self):
        return self.descripcion

    @property
    def is_active(self):
        return self.activa

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class NewsArticle(models.Model):
    """
    Tabla SQL (AMP-01): plus.noticias
    """

    class EstadoPublicacion(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        EN_REVISION = 'en_revision', 'En revisión'
        PUBLICADA = 'publicada', 'Publicada'
        ARCHIVADA = 'archivada', 'Archivada'

    class PublicationStatus(models.TextChoices):
        DRAFT = 'borrador', 'Borrador'
        IN_REVIEW = 'en_revision', 'En revisión'
        PUBLISHED = 'publicada', 'Publicada'
        ARCHIVED = 'archivada', 'Archivada'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_noticia',
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_autor',
        related_name='noticias_creadas',
    )
    categoria = models.ForeignKey(
        NewsCategory,
        on_delete=models.RESTRICT,
        db_column='id_categoria',
        related_name='noticias',
    )
    iniciativa_relacionada = models.ForeignKey(
        'initiatives.Initiative',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_iniciativa',
        related_name='noticias_asociadas',
    )
    titulo = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    extracto = models.TextField()
    contenido = models.TextField()
    estado_publicacion = models.CharField(
        max_length=20,
        choices=EstadoPublicacion.choices,
        default=EstadoPublicacion.BORRADOR,
    )
    destacada = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'noticias'
        ordering = ['-fecha_publicacion', '-fecha_creacion']
        indexes = [
            models.Index(
                fields=['estado_publicacion', '-fecha_publicacion'],
                name='ix_noticias_pub_fecha',
            ),
        ]

    def __init__(self, *args, **kwargs):
        alias_map = {
            'title': 'titulo',
            'summary': 'extracto',
            'resumen': 'extracto',
            'descripcion_corta': 'extracto',
            'content': 'contenido',
            'author': 'autor',
            'category': 'categoria',
            'related_initiative': 'iniciativa_relacionada',
            'is_featured': 'destacada',
            'published_at': 'fecha_publicacion',
        }
        for eng, esp in alias_map.items():
            if eng in kwargs and esp not in kwargs:
                kwargs[esp] = kwargs.pop(eng)
        if 'publication_status' in kwargs and 'estado_publicacion' not in kwargs:
            val = str(kwargs.pop('publication_status')).lower()
            status_map = {
                'draft': 'borrador',
                'published': 'publicada',
                'archived': 'archivada',
            }
            kwargs['estado_publicacion'] = status_map.get(val, val)
        super().__init__(*args, **kwargs)

    @property
    def id_noticia(self):
        return self.id

    @property
    def title(self):
        return self.titulo

    @property
    def summary(self):
        return self.extracto

    @property
    def content(self):
        return self.contenido

    @property
    def author(self):
        return self.autor

    @property
    def category(self):
        return self.categoria

    @property
    def related_initiative(self):
        return self.iniciativa_relacionada

    @property
    def publication_status(self):
        return self.estado_publicacion

    @property
    def is_featured(self):
        return self.destacada

    @property
    def published_at(self):
        return self.fecha_publicacion

    @property
    def created_at(self):
        return self.fecha_creacion

    @property
    def updated_at(self):
        return self.fecha_actualizacion

    @property
    def portada(self):
        return self.multimedia.filter(es_portada=True).first() or self.multimedia.first()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo) or 'noticia'
            slug = base_slug
            counter = 1
            while NewsArticle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        if self.estado_publicacion == self.EstadoPublicacion.PUBLICADA and not self.fecha_publicacion:
            self.fecha_publicacion = timezone.now()
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class NewsMedia(models.Model):
    """
    Tabla SQL (AMP-01): plus.noticia_multimedia
    """

    class TipoArchivo(models.TextChoices):
        IMAGEN = 'imagen', 'Imagen'
        VIDEO = 'video', 'Video'
        DOCUMENTO = 'documento', 'Documento'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id_multimedia',
    )
    noticia = models.ForeignKey(
        NewsArticle,
        on_delete=models.CASCADE,
        db_column='id_noticia',
        related_name='multimedia',
    )
    tipo_archivo = models.CharField(
        max_length=20,
        choices=TipoArchivo.choices,
        default=TipoArchivo.IMAGEN,
    )
    ruta_archivo = models.TextField()
    texto_alternativo = models.CharField(max_length=250, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    orden = models.IntegerField(default=0)
    es_portada = models.BooleanField(default=False)
    fecha_carga = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'noticia_multimedia'
        ordering = ['orden', '-fecha_carga']
        constraints = [
            models.UniqueConstraint(
                fields=['noticia'],
                condition=Q(es_portada=True),
                name='ux_noticia_portada_unica',
            ),
        ]

    @property
    def id_multimedia(self):
        return self.id

    def __str__(self):
        return f'Multimedia {self.tipo_archivo} de {self.noticia.titulo}'
