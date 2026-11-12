import os
import re
import uuid
from django.core.files.storage import default_storage
from rest_framework import serializers
from apps.initiatives.models import (
    Initiative,
    InitiativeActivity,
    InitiativeCaseLink,
    InitiativeCommunity,
    InitiativeEdition,
    InitiativeMedia,
    InitiativeMetric,
)


class InitiativeMetricSerializer(serializers.ModelSerializer):
    id_indicador = serializers.UUIDField(source='id', read_only=True)
    label = serializers.CharField(source='nombre', required=False)
    value = serializers.DecimalField(source='valor', max_digits=14, decimal_places=2, required=False)

    class Meta:
        model = InitiativeMetric
        fields = [
            'id',
            'id_indicador',
            'edicion',
            'nombre',
            'label',
            'valor',
            'value',
            'unidad',
            'descripcion',
            'icono',
            'tipo_medicion',
            'orden',
            'fecha_corte',
        ]
        extra_kwargs = {
            'nombre': {'required': False},
            'valor': {'required': False},
        }


class InitiativeMediaSerializer(serializers.ModelSerializer):
    """P21: Soporte completo multipart/form-data con validación binaria, sanitización y URL pública."""
    id_multimedia = serializers.UUIDField(source='id', read_only=True)
    file = serializers.FileField(write_only=True, required=False)
    archivo = serializers.FileField(write_only=True, required=False)
    ruta_archivo = serializers.CharField(required=False, allow_blank=True)
    url = serializers.SerializerMethodField(read_only=True)
    url_archivo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InitiativeMedia
        fields = [
            'id',
            'id_multimedia',
            'iniciativa',
            'edicion',
            'tipo',
            'file',
            'archivo',
            'ruta_archivo',
            'url',
            'url_archivo',
            'texto_alternativo',
            'descripcion',
            'es_portada',
            'orden',
            'fecha_subida',
        ]
        read_only_fields = ['id', 'id_multimedia', 'fecha_subida', 'url', 'url_archivo']

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
                '.jpg': InitiativeMedia.Tipo.IMAGEN,
                '.jpeg': InitiativeMedia.Tipo.IMAGEN,
                '.png': InitiativeMedia.Tipo.IMAGEN,
                '.webp': InitiativeMedia.Tipo.IMAGEN,
                '.gif': InitiativeMedia.Tipo.IMAGEN,
                '.mp4': InitiativeMedia.Tipo.VIDEO,
                '.mov': InitiativeMedia.Tipo.VIDEO,
                '.webm': InitiativeMedia.Tipo.VIDEO,
                '.pdf': InitiativeMedia.Tipo.DOCUMENTO,
            }
            if ext not in allowed_exts:
                raise serializers.ValidationError(
                    {'file': f'Formato no permitido ({ext}). Formatos válidos: JPG, PNG, WEBP, MP4, PDF.'}
                )
            if uploaded.size > 15 * 1024 * 1024:
                raise serializers.ValidationError(
                    {'file': 'El archivo supera el tamaño máximo permitido de 15 MB.'}
                )

            # Auto-inferir tipo si no fue especificado
            if not attrs.get('tipo'):
                attrs['tipo'] = allowed_exts[ext]

            iniciativa = attrs.get('iniciativa') or (self.instance.iniciativa if self.instance else None)
            ini_id = str(iniciativa.id) if iniciativa else 'general'
            short_id = uuid.uuid4().hex[:8]
            safe_filename = f"{os.path.splitext(clean_name)[0]}_{short_id}{ext}"
            save_path = f"initiatives/{ini_id}/{safe_filename}"
            saved = default_storage.save(save_path, uploaded)
            attrs['ruta_archivo'] = saved

        # Validar regla de base de datos ck_portada_imagen: (NOT es_portada OR tipo = 'imagen')
        if attrs.get('es_portada') and attrs.get('tipo', getattr(self.instance, 'tipo', None)) != InitiativeMedia.Tipo.IMAGEN:
            raise serializers.ValidationError(
                {'es_portada': 'Solo los archivos de tipo imagen pueden marcarse como portada.'}
            )

        # Validar que si se envía edición, pertenezca a la iniciativa
        edicion = attrs.get('edicion')
        iniciativa = attrs.get('iniciativa') or (self.instance.iniciativa if self.instance else None)
        if edicion and iniciativa and edicion.iniciativa_id != iniciativa.id:
            raise serializers.ValidationError(
                {'edicion': 'La edición seleccionada no pertenece a la iniciativa especificada.'}
            )

        return attrs

    def create(self, validated_data):
        if validated_data.get('es_portada') and validated_data.get('iniciativa'):
            InitiativeMedia.objects.filter(
                iniciativa=validated_data['iniciativa'],
                es_portada=True,
            ).update(es_portada=False)
        return super().create(validated_data)


class InitiativeActivitySerializer(serializers.ModelSerializer):
    id_actividad = serializers.UUIDField(source='id', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)
    responsable_nombre = serializers.CharField(source='responsable.full_name', read_only=True)

    class Meta:
        model = InitiativeActivity
        fields = [
            'id',
            'id_actividad',
            'edicion',
            'responsable',
            'responsable_nombre',
            'comunidad',
            'comunidad_nombre',
            'titulo',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'lugar',
            'ubicacion',
            'estado',
            'fecha_creacion',
        ]
        read_only_fields = ['id', 'id_actividad', 'fecha_creacion']


class InitiativeCommunitySerializer(serializers.ModelSerializer):
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)

    class Meta:
        model = InitiativeCommunity
        fields = ['id', 'edicion', 'comunidad', 'comunidad_nombre', 'observaciones']


class InitiativeCaseLinkSerializer(serializers.ModelSerializer):
    caso_codigo = serializers.CharField(source='caso.codigo', read_only=True)

    class Meta:
        model = InitiativeCaseLink
        fields = ['id', 'edicion', 'caso', 'caso_codigo', 'tipo_vinculo', 'observaciones', 'fecha_vinculacion']


class InitiativeEditionSerializer(serializers.ModelSerializer):
    id_edicion = serializers.UUIDField(source='id', read_only=True)
    indicadores = InitiativeMetricSerializer(many=True, read_only=True)
    actividades = InitiativeActivitySerializer(many=True, read_only=True)
    comunidades_vinculadas = InitiativeCommunitySerializer(many=True, read_only=True)
    casos_vinculados = InitiativeCaseLinkSerializer(many=True, read_only=True)

    class Meta:
        model = InitiativeEdition
        fields = [
            'id',
            'id_edicion',
            'iniciativa',
            'anio',
            'nombre_edicion',
            'temporada',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'indicadores',
            'actividades',
            'comunidades_vinculadas',
            'casos_vinculados',
            'fecha_creacion',
        ]
        read_only_fields = ['id', 'id_edicion', 'fecha_creacion']


class InitiativeListSerializer(serializers.ModelSerializer):
    """
    Contrato alineado con vw_iniciativas_destacadas y el catálogo público de Angular.
    """
    id_iniciativa = serializers.UUIDField(source='id', read_only=True)
    name = serializers.CharField(source='titulo', read_only=True)
    featured_title = serializers.CharField(source='subtitulo', read_only=True)
    short_description = serializers.CharField(source='descripcion_corta', read_only=True)
    portada = serializers.SerializerMethodField()
    metrics = serializers.SerializerMethodField()

    class Meta:
        model = Initiative
        fields = [
            'id',
            'id_iniciativa',
            'titulo',
            'name',
            'subtitulo',
            'featured_title',
            'slug',
            'descripcion_corta',
            'short_description',
            'categoria',
            'estado',
            'estado_publicacion',
            'destacada',
            'orden_destacado',
            'fecha_publicacion',
            'portada',
            'metrics',
        ]
        read_only_fields = fields

    def get_portada(self, obj):
        cover = obj.multimedia.filter(es_portada=True, edicion__isnull=True).first()
        return cover.ruta_archivo if cover else None

    def get_metrics(self, obj):
        qs = InitiativeMetric.objects.filter(edicion__iniciativa=obj).order_by('orden')
        return InitiativeMetricSerializer(qs, many=True).data


class PublicInitiativeActivitySerializer(serializers.ModelSerializer):
    """P19: Proyección pública mínima de actividades (sin responsable ni coordenadas GeoJSON internas)."""
    id_actividad = serializers.UUIDField(source='id', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)

    class Meta:
        model = InitiativeActivity
        fields = [
            'id',
            'id_actividad',
            'titulo',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'lugar',
            'comunidad_nombre',
            'estado',
        ]
        read_only_fields = fields


class PublicInitiativeEditionSerializer(serializers.ModelSerializer):
    """P19: Proyección pública autorizada de edición de iniciativa (sin casos internos ni responsables)."""
    id_edicion = serializers.UUIDField(source='id', read_only=True)
    indicadores = InitiativeMetricSerializer(many=True, read_only=True)
    actividades = PublicInitiativeActivitySerializer(many=True, read_only=True)

    class Meta:
        model = InitiativeEdition
        fields = [
            'id',
            'id_edicion',
            'anio',
            'nombre_edicion',
            'temporada',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'indicadores',
            'actividades',
        ]
        read_only_fields = fields


class InitiativeDetailSerializer(InitiativeListSerializer):
    ediciones = PublicInitiativeEditionSerializer(many=True, read_only=True)
    multimedia = InitiativeMediaSerializer(many=True, read_only=True)

    class Meta(InitiativeListSerializer.Meta):
        fields = InitiativeListSerializer.Meta.fields + [
            'descripcion',
            'ediciones',
            'multimedia',
            'fecha_creacion',
            'fecha_actualizacion',
        ]


class AdminInitiativeSerializer(serializers.ModelSerializer):
    id_iniciativa = serializers.UUIDField(source='id', read_only=True)
    name = serializers.CharField(source='titulo', required=False)
    featured_title = serializers.CharField(source='subtitulo', required=False, allow_blank=True)
    short_description = serializers.CharField(source='descripcion_corta', required=False, allow_blank=True)
    full_content = serializers.CharField(source='descripcion', required=False, allow_blank=True)
    category = serializers.CharField(source='categoria', required=False)
    is_featured = serializers.BooleanField(source='destacada', required=False)
    publication_status = serializers.CharField(write_only=True, required=False)
    ediciones = InitiativeEditionSerializer(many=True, read_only=True)
    multimedia = InitiativeMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Initiative
        fields = [
            'id',
            'id_iniciativa',
            'creador',
            'titulo',
            'name',
            'subtitulo',
            'featured_title',
            'slug',
            'descripcion_corta',
            'short_description',
            'descripcion',
            'full_content',
            'categoria',
            'category',
            'estado',
            'estado_publicacion',
            'publication_status',
            'destacada',
            'is_featured',
            'orden_destacado',
            'ediciones',
            'multimedia',
            'fecha_creacion',
            'fecha_actualizacion',
            'fecha_publicacion',
        ]
        read_only_fields = ['id', 'id_iniciativa', 'creador', 'slug', 'fecha_creacion', 'fecha_actualizacion', 'fecha_publicacion']
        extra_kwargs = {
            'titulo': {'required': False},
            'categoria': {'required': False},
        }

    def validate(self, attrs):
        pub_alias = attrs.pop('publication_status', None)
        if pub_alias:
            pub_map = {
                'PUBLISHED': Initiative.EstadoPublicacion.PUBLICADA,
                'PUBLICADA': Initiative.EstadoPublicacion.PUBLICADA,
                'DRAFT': Initiative.EstadoPublicacion.BORRADOR,
                'BORRADOR': Initiative.EstadoPublicacion.BORRADOR,
                'PENDING': Initiative.EstadoPublicacion.PENDIENTE,
                'PENDIENTE': Initiative.EstadoPublicacion.PENDIENTE,
                'REJECTED': Initiative.EstadoPublicacion.RECHAZADA,
                'RECHAZADA': Initiative.EstadoPublicacion.RECHAZADA,
            }
            attrs['estado_publicacion'] = pub_map.get(pub_alias.upper(), pub_alias.lower())

        if not self.instance:
            if not attrs.get('titulo'):
                raise serializers.ValidationError({'titulo': 'El título de la iniciativa es obligatorio.'})
            if not attrs.get('categoria'):
                attrs['categoria'] = 'general'
        return attrs
