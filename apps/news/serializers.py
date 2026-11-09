from rest_framework import serializers
from apps.news.models import NewsArticle, NewsCategory, NewsMedia


class NewsMediaSerializer(serializers.ModelSerializer):
    id_multimedia = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = NewsMedia
        fields = [
            'id',
            'id_multimedia',
            'noticia',
            'tipo_archivo',
            'ruta_archivo',
            'texto_alternativo',
            'descripcion',
            'orden',
            'es_portada',
            'fecha_carga',
        ]
        read_only_fields = ['id', 'id_multimedia', 'fecha_carga']


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
