from rest_framework import serializers
from apps.cases.models import Case, CaseAssignment, CaseCategory, CaseEvidence, CaseStatus
from apps.territories.models import Community
from apps.tracking.serializers import (
    CaseStatusHistorySerializer,
    CaseUpdateSerializer,
    PublicCaseStatusHistorySerializer,
    PublicCaseUpdateSerializer,
)
from core.gis import make_geojson_point


class CaseCategorySerializer(serializers.ModelSerializer):
    id_tipo_caso = serializers.UUIDField(source='id', read_only=True)
    casos_count = serializers.IntegerField(source='casos.count', read_only=True)

    class Meta:
        model = CaseCategory
        fields = [
            'id',
            'id_tipo_caso',
            'nombre',
            'descripcion',
            'categoria',
            'activo',
            'casos_count',
        ]


class CaseStatusSerializer(serializers.ModelSerializer):
    id_estado = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = CaseStatus
        fields = ['id', 'id_estado', 'nombre', 'descripcion', 'orden']


class CaseEvidenceSerializer(serializers.ModelSerializer):
    id_evidencia = serializers.UUIDField(source='id', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.full_name', read_only=True)

    class Meta:
        model = CaseEvidence
        fields = [
            'id',
            'id_evidencia',
            'caso',
            'usuario',
            'usuario_nombre',
            'tipo_archivo',
            'ruta_archivo',
            'descripcion',
            'fecha_subida',
        ]
        read_only_fields = ['id', 'id_evidencia', 'caso', 'usuario', 'usuario_nombre', 'fecha_subida']


class CaseAssignmentSerializer(serializers.ModelSerializer):
    id_asignacion_caso = serializers.UUIDField(source='id', read_only=True)
    responsable_nombre = serializers.CharField(source='responsable.full_name', read_only=True)
    responsable_correo = serializers.CharField(source='responsable.correo', read_only=True)
    asignador_nombre = serializers.CharField(source='asignador.full_name', read_only=True)

    class Meta:
        model = CaseAssignment
        fields = [
            'id',
            'id_asignacion_caso',
            'caso',
            'responsable',
            'responsable_nombre',
            'responsable_correo',
            'asignador',
            'asignador_nombre',
            'fecha_asignacion',
            'fecha_finalizacion',
            'activo',
        ]
        read_only_fields = fields


class PublicCaseListSerializer(serializers.ModelSerializer):
    """
    Serializador público para casos aprobados (`estado_publicacion='aprobado'`).
    No expone datos personales del ciudadano (`id_usuario`) y devuelve coordenadas generalizadas.
    """
    id_caso = serializers.UUIDField(source='id', read_only=True)
    radicado_code = serializers.CharField(source='codigo', read_only=True)
    tipo_nombre = serializers.CharField(source='tipo_caso.nombre', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)
    municipio_nombre = serializers.CharField(source='comunidad.municipio.nombre', read_only=True)
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    public_location = serializers.ReadOnlyField()

    class Meta:
        model = Case
        fields = [
            'id',
            'id_caso',
            'codigo',
            'radicado_code',
            'titulo',
            'tipo_caso',
            'tipo_nombre',
            'comunidad',
            'comunidad_nombre',
            'municipio_nombre',
            'estado',
            'estado_nombre',
            'prioridad',
            'estado_publicacion',
            'public_location',
            'fecha_creacion',
            'fecha_aprobacion',
        ]
        read_only_fields = fields


class PublicCaseDetailSerializer(PublicCaseListSerializer):
    public_updates = serializers.SerializerMethodField()
    public_status_history = serializers.SerializerMethodField()
    approved_comments = serializers.SerializerMethodField()

    class Meta(PublicCaseListSerializer.Meta):
        fields = PublicCaseListSerializer.Meta.fields + [
            'descripcion',
            'public_updates',
            'public_status_history',
            'approved_comments',
        ]

    def get_public_updates(self, obj):
        qs = obj.seguimientos.filter(visible_publicamente=True)
        return PublicCaseUpdateSerializer(qs, many=True).data

    def get_public_status_history(self, obj):
        qs = obj.historial_estados.select_related('estado_anterior', 'estado_nuevo').all()
        return PublicCaseStatusHistorySerializer(qs, many=True).data

    def get_approved_comments(self, obj):
        from apps.communications.models import CaseComment
        from apps.communications.serializers import PublicCaseCommentSerializer

        qs = obj.comentarios.filter(estado_moderacion=CaseComment.EstadoModeracion.APROBADO).select_related('usuario')
        return PublicCaseCommentSerializer(qs, many=True).data


class CitizenCaseCreateUpdateSerializer(serializers.ModelSerializer):
    id_caso = serializers.UUIDField(source='id', read_only=True)
    radicado_code = serializers.CharField(source='codigo', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        source='tipo_caso',
        queryset=CaseCategory.objects.filter(activo=True),
        required=False,
    )
    community = serializers.PrimaryKeyRelatedField(
        source='comunidad',
        queryset=Community.objects.filter(activo=True),
        required=False,
    )
    title = serializers.CharField(source='titulo', required=False)
    description = serializers.CharField(source='descripcion', required=False)
    exact_latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, write_only=True)
    exact_longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, write_only=True)
    latitud = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, write_only=True)
    longitud = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, write_only=True)
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    moderation_status = serializers.CharField(source='estado_publicacion', read_only=True)
    management_status = serializers.CharField(source='estado.nombre', read_only=True)
    seguimientos = CaseUpdateSerializer(many=True, read_only=True)
    evidencias = CaseEvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = [
            'id',
            'id_caso',
            'codigo',
            'radicado_code',
            'titulo',
            'title',
            'descripcion',
            'description',
            'tipo_caso',
            'category',
            'comunidad',
            'community',
            'estado',
            'estado_nombre',
            'management_status',
            'prioridad',
            'estado_publicacion',
            'moderation_status',
            'ubicacion',
            'exact_latitude',
            'exact_longitude',
            'latitud',
            'longitud',
            'direccion_referencia',
            'seguimientos',
            'evidencias',
            'fecha_creacion',
            'fecha_actualizacion',
            'fecha_aprobacion',
        ]
        read_only_fields = [
            'id',
            'id_caso',
            'codigo',
            'radicado_code',
            'estado',
            'estado_nombre',
            'management_status',
            'prioridad',
            'estado_publicacion',
            'moderation_status',
            'fecha_creacion',
            'fecha_actualizacion',
            'fecha_aprobacion',
        ]
        extra_kwargs = {
            'titulo': {'required': False},
            'descripcion': {'required': False},
            'tipo_caso': {'required': False},
            'comunidad': {'required': False},
        }

    def validate(self, attrs):
        if not self.instance:
            if not attrs.get('titulo'):
                raise serializers.ValidationError({'titulo': 'El título del caso es obligatorio.'})
            if not attrs.get('descripcion'):
                raise serializers.ValidationError({'descripcion': 'La descripción del caso es obligatoria.'})
            if not attrs.get('tipo_caso'):
                raise serializers.ValidationError({'tipo_caso': 'Debe seleccionar el tipo de caso.'})
            if not attrs.get('comunidad'):
                raise serializers.ValidationError({'comunidad': 'Debe seleccionar la comunidad.'})

        lat = attrs.pop('latitud', None) or attrs.pop('exact_latitude', None)
        lon = attrs.pop('longitud', None) or attrs.pop('exact_longitude', None)
        if lat is not None and lon is not None and not attrs.get('ubicacion'):
            attrs['ubicacion'] = make_geojson_point(lon, lat)
        return attrs


class AdminCaseDetailSerializer(serializers.ModelSerializer):
    id_caso = serializers.UUIDField(source='id', read_only=True)
    radicado_code = serializers.CharField(source='codigo', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.full_name', read_only=True)
    usuario_correo = serializers.CharField(source='usuario.correo', read_only=True)
    tipo_nombre = serializers.CharField(source='tipo_caso.nombre', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)
    municipio_nombre = serializers.CharField(source='comunidad.municipio.nombre', read_only=True)
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    moderation_status = serializers.CharField(source='estado_publicacion', read_only=True)
    management_status = serializers.CharField(source='estado.nombre', read_only=True)
    active_assignment = CaseAssignmentSerializer(read_only=True)
    asignaciones = CaseAssignmentSerializer(many=True, read_only=True)
    seguimientos = CaseUpdateSerializer(many=True, read_only=True)
    historial_estados = CaseStatusHistorySerializer(many=True, read_only=True)
    evidencias = CaseEvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = [
            'id',
            'id_caso',
            'codigo',
            'radicado_code',
            'usuario',
            'usuario_nombre',
            'usuario_correo',
            'tipo_caso',
            'tipo_nombre',
            'comunidad',
            'comunidad_nombre',
            'municipio_nombre',
            'estado',
            'estado_nombre',
            'management_status',
            'prioridad',
            'estado_publicacion',
            'moderation_status',
            'ubicacion',
            'direccion_referencia',
            'active_assignment',
            'asignaciones',
            'seguimientos',
            'historial_estados',
            'evidencias',
            'fecha_creacion',
            'fecha_actualizacion',
            'fecha_aprobacion',
        ]
        read_only_fields = ['id', 'id_caso', 'codigo', 'usuario', 'fecha_creacion', 'fecha_actualizacion']


class CaseModerationActionSerializer(serializers.Serializer):
    estado_publicacion = serializers.CharField(required=False)
    moderation_status = serializers.CharField(required=False)
    motivo = serializers.CharField(required=False, allow_blank=True, default='')
    moderation_reason = serializers.CharField(required=False, allow_blank=True, default='')
    prioridad = serializers.CharField(required=False)
    priority = serializers.CharField(required=False)

    def validate(self, attrs):
        pub = attrs.get('estado_publicacion') or attrs.get('moderation_status')
        if not pub:
            raise serializers.ValidationError({'estado_publicacion': 'Debe indicar el nuevo estado de publicación.'})
        attrs['resolved_pub'] = pub
        attrs['resolved_motivo'] = attrs.get('motivo') or attrs.get('moderation_reason') or ''
        attrs['resolved_prio'] = attrs.get('prioridad') or attrs.get('priority')
        return attrs


class CaseAssignResponsibleSerializer(serializers.Serializer):
    id_responsable = serializers.UUIDField(required=False)
    assigned_to = serializers.UUIDField(required=False)

    def validate(self, attrs):
        resp_id = attrs.get('id_responsable') or attrs.get('assigned_to')
        if not resp_id:
            raise serializers.ValidationError({'id_responsable': 'Debe indicar el UUID del responsable.'})
        attrs['resolved_responsable_id'] = resp_id
        return attrs


class CaseManagementStatusSerializer(serializers.Serializer):
    estado = serializers.CharField(required=False)
    management_status = serializers.CharField(required=False)
    motivo = serializers.CharField(required=False, allow_blank=True, default='')
    observations = serializers.CharField(required=False, allow_blank=True, default='')
    final_result = serializers.CharField(required=False, allow_blank=True, default='')

    def validate(self, attrs):
        st = attrs.get('estado') or attrs.get('management_status')
        if not st:
            raise serializers.ValidationError({'estado': 'Debe indicar el nuevo estado operativo.'})
        attrs['resolved_status'] = st
        attrs['resolved_motivo'] = (
            attrs.get('motivo')
            or attrs.get('final_result')
            or attrs.get('observations')
            or ''
        )
        return attrs


class CaseUpdateCreateSerializer(serializers.Serializer):
    descripcion = serializers.CharField(required=False)
    title = serializers.CharField(required=False, allow_blank=True)
    content = serializers.CharField(required=False, allow_blank=True)
    visible_publicamente = serializers.BooleanField(required=False)
    visibility = serializers.CharField(required=False)

    def validate(self, attrs):
        desc = attrs.get('descripcion')
        if not desc:
            title = attrs.get('title', '').strip()
            content = attrs.get('content', '').strip()
            desc = f'{title}: {content}'.strip(': ') if title else content
        if not desc:
            raise serializers.ValidationError({'descripcion': 'La descripción del seguimiento es obligatoria.'})
        attrs['resolved_descripcion'] = desc
        if 'visible_publicamente' in attrs:
            attrs['resolved_visible'] = bool(attrs['visible_publicamente'])
        else:
            attrs['resolved_visible'] = str(attrs.get('visibility', '')).upper() == 'PUBLIC'
        return attrs
