import os
import re
import uuid
from django.core.files.storage import default_storage
from rest_framework import serializers
from apps.news.models import NewsArticle, NewsCategory, NewsMedia


class NewsMediaSerializer(serializers.ModelSerializer):
    """P21: Soporte completo multipart/form-data con validación binaria, sanitización y URL pública."""
    id_multimedia = serializers.UUIDField(source='id', read_only=True)
    file = serializers.FileField(write_only=True, required=False)
    archivo = serializers.FileField(write_only=True, required=False)
    ruta_archivo = serializers.CharField(required=False, allow_blank=True)
    url = serializers.SerializerMethodField(read_only=True)
    url_archivo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NewsMedia
        fields = [
            'id',
            'id_multimedia',
            'noticia',
            'tipo_archivo',
            'file',
            'archivo',
            'ruta_archivo',
            'url',
            'url_archivo',
            'texto_alternativo',
            'descripcion',
            'orden',
            'es_portada',
            'fecha_carga',
        ]
        read_only_fields = ['id', 'id_multimedia', 'fecha_carga', 'url', 'url_archivo']

    def get_url(self, obj) -> str:
        if not obj.ruta_archivo:
            return ''
        request = self.context.get('request')
        path = f'/api/v1/public/media/{obj.ruta_archivo.lstrip("/")}'
        return request.build_absolute_uri(path) if request else path

    def get_url_archivo(self, obj) -> str:
        return self.get_url(obj)

    def validate(self, attrs):
        request = self.context.get('request')
        uploaded = (
            attrs.pop('file', None)
            or attrs.pop('archivo', None)
            or (request.FILES.get('file') if request else None)
            or (request.FILES.get('archivo') if request else None)
        )
        ruta = attrs.get('ruta_archivo') or (self.instance.ruta_archivo if self.instance else None)

        if not uploaded and not ruta:
            raise serializers.ValidationError(
                {'file': 'Debes enviar un archivo mediante "file" o proporcionar "ruta_archivo".'}
            )

        if uploaded:
            clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', os.path.basename(uploaded.name))
            ext = os.path.splitext(clean_name)[1].lower()
            allowed_exts = {
                '.jpg': NewsMedia.TipoArchivo.IMAGEN,
                '.jpeg': NewsMedia.TipoArchivo.IMAGEN,
                '.png': NewsMedia.TipoArchivo.IMAGEN,
                '.webp': NewsMedia.TipoArchivo.IMAGEN,
                '.gif': NewsMedia.TipoArchivo.IMAGEN,
                '.mp4': NewsMedia.TipoArchivo.VIDEO,
                '.mov': NewsMedia.TipoArchivo.VIDEO,
                '.webm': NewsMedia.TipoArchivo.VIDEO,
                '.pdf': NewsMedia.TipoArchivo.DOCUMENTO,
            }
            if ext not in allowed_exts:
                raise serializers.ValidationError(
                    {'file': f'Formato no permitido ({ext}). Formatos válidos: JPG, PNG, WEBP, MP4, PDF.'}
                )
            if uploaded.size > 15 * 1024 * 1024:
                raise serializers.ValidationError(
                    {'file': 'El archivo supera el tamaño máximo permitido de 15 MB.'}
                )

            if not attrs.get('tipo_archivo'):
                attrs['tipo_archivo'] = allowed_exts[ext]

            noticia = attrs.get('noticia') or (self.instance.noticia if self.instance else None)
            noticia_id = str(noticia.id) if noticia else 'general'
            short_id = uuid.uuid4().hex[:8]
            safe_filename = f"{os.path.splitext(clean_name)[0]}_{short_id}{ext}"
            save_path = f"news/{noticia_id}/{safe_filename}"
            saved = default_storage.save(save_path, uploaded)
            attrs['ruta_archivo'] = saved

        return attrs

    def create(self, validated_data):
        if validated_data.get('es_portada') and validated_data.get('noticia'):
            NewsMedia.objects.filter(
                noticia=validated_data['noticia'],
                es_portada=True,
            ).update(es_portada=False)
        return super().create(validated_data)


class NewsCategorySerializer(serializers.ModelSerializer):
    id_categoria_noticia = serializers.UUIDField(source='id', read_only=True)
    name = serializers.CharField(source='nombre', required=False)
    description = serializers.CharField(source='descripcion', required=False, allow_blank=True)
    is_active = serializers.BooleanField(source='activa', required=False)
    articles_count = serializers.IntegerField(source='noticias.count', read_only=True)

    class Meta:
        model = NewsCategory
        fields = [
            'id',
            'id_categoria_noticia',
            'nombre',
            'name',
            'slug',
            'descripcion',
            'description',
            'activa',
            'is_active',
            'articles_count',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = ['id', 'id_categoria_noticia', 'slug', 'articles_count', 'fecha_creacion', 'fecha_actualizacion']
        extra_kwargs = {
            'nombre': {'required': False},
        }


class NewsArticleListSerializer(serializers.ModelSerializer):
    id_noticia = serializers.UUIDField(source='id', read_only=True)
    title = serializers.CharField(source='titulo', read_only=True)
    summary = serializers.CharField(source='extracto', read_only=True)
    category = serializers.UUIDField(source='categoria_id', read_only=True)
    category_name = serializers.CharField(source='categoria.nombre', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    author = serializers.UUIDField(source='autor_id', read_only=True)
    author_name = serializers.CharField(source='autor.full_name', read_only=True)
    autor_nombre = serializers.CharField(source='autor.full_name', read_only=True)
    related_initiative = serializers.UUIDField(source='iniciativa_relacionada_id', read_only=True)
    related_initiative_name = serializers.CharField(source='iniciativa_relacionada.titulo', read_only=True)
    related_initiative_slug = serializers.CharField(source='iniciativa_relacionada.slug', read_only=True)
    publication_status = serializers.CharField(source='estado_publicacion', read_only=True)
    is_featured = serializers.BooleanField(source='destacada', read_only=True)
    published_at = serializers.DateTimeField(source='fecha_publicacion', read_only=True)
    created_at = serializers.DateTimeField(source='fecha_creacion', read_only=True)
    portada = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            'id',
            'id_noticia',
            'titulo',
            'title',
            'slug',
            'extracto',
            'summary',
            'portada',
            'categoria',
            'category',
            'categoria_nombre',
            'category_name',
            'iniciativa_relacionada',
            'related_initiative',
            'related_initiative_name',
            'related_initiative_slug',
            'autor',
            'author',
            'autor_nombre',
            'author_name',
            'estado_publicacion',
            'publication_status',
            'destacada',
            'is_featured',
            'fecha_publicacion',
            'published_at',
            'fecha_creacion',
            'created_at',
        ]
        read_only_fields = fields

    def get_portada(self, obj):
        cover = obj.portada
        return cover.ruta_archivo if cover else None


class NewsArticleDetailSerializer(serializers.ModelSerializer):
    id_noticia = serializers.UUIDField(source='id', read_only=True)
    title = serializers.CharField(source='titulo', required=False)
    summary = serializers.CharField(source='extracto', required=False)
    content = serializers.CharField(source='contenido', required=False)
    category = serializers.PrimaryKeyRelatedField(
        source='categoria',
        queryset=NewsCategory.objects.all(),
        required=False,
    )
    related_initiative = serializers.UUIDField(source='iniciativa_relacionada_id', required=False, allow_null=True)
    is_featured = serializers.BooleanField(source='destacada', required=False)
    publication_status = serializers.CharField(write_only=True, required=False)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    category_name = serializers.CharField(source='categoria.nombre', read_only=True)
    autor_nombre = serializers.CharField(source='autor.full_name', read_only=True)
    author_name = serializers.CharField(source='autor.full_name', read_only=True)
    multimedia = NewsMediaSerializer(many=True, read_only=True)
    portada = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            'id',
            'id_noticia',
            'titulo',
            'title',
            'slug',
            'extracto',
            'summary',
            'contenido',
            'content',
            'portada',
            'multimedia',
            'categoria',
            'category',
            'categoria_nombre',
            'category_name',
            'iniciativa_relacionada',
            'related_initiative',
            'autor',
            'autor_nombre',
            'author_name',
            'estado_publicacion',
            'publication_status',
            'destacada',
            'is_featured',
            'fecha_publicacion',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = [
            'id',
            'id_noticia',
            'slug',
            'portada',
            'multimedia',
            'categoria_nombre',
            'category_name',
            'autor',
            'autor_nombre',
            'author_name',
            'fecha_publicacion',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        extra_kwargs = {
            'titulo': {'required': False},
            'extracto': {'required': False},
            'contenido': {'required': False},
            'categoria': {'required': False},
        }

    def get_portada(self, obj):
        cover = obj.portada
        return cover.ruta_archivo if cover else None

    def validate(self, attrs):
        pub = attrs.pop('publication_status', None)
        if pub:
            status_map = {
                'draft': NewsArticle.EstadoPublicacion.BORRADOR,
                'borrador': NewsArticle.EstadoPublicacion.BORRADOR,
                'in_review': NewsArticle.EstadoPublicacion.EN_REVISION,
                'en_revision': NewsArticle.EstadoPublicacion.EN_REVISION,
                'published': NewsArticle.EstadoPublicacion.PUBLICADA,
                'publicada': NewsArticle.EstadoPublicacion.PUBLICADA,
                'archived': NewsArticle.EstadoPublicacion.ARCHIVADA,
                'archivada': NewsArticle.EstadoPublicacion.ARCHIVADA,
            }
            attrs['estado_publicacion'] = status_map.get(pub.lower(), pub.lower())
        return attrs
