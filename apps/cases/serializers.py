from rest_framework import serializers
from apps.cases.models import (
    Case,
    CaseAssignment,
    CaseCategory,
    CaseContribution,
    CaseCorrectionRequest,
    CaseEvidence,
    CaseStatus,
    FollowedCase,
)
from apps.cases.services import CaseService
from apps.territories.models import Community
from apps.tracking.models import CaseUpdate
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
            'naturaleza',
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
    id_aporte = serializers.UUIDField(source='aporte_id', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.full_name', read_only=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = CaseEvidence
        fields = [
            'id',
            'id_evidencia',
            'caso',
            'usuario',
            'usuario_nombre',
            'id_aporte',
            'tipo_archivo',
            'ruta_archivo',
            'download_url',
            'descripcion',
            'audiencia',
            'estado_revision',
            'nombre_original',
            'mime_type',
            'tamano_bytes',
            'fecha_subida',
        ]
        read_only_fields = [
            'id',
            'id_evidencia',
            'caso',
            'usuario',
            'usuario_nombre',
            'id_aporte',
            'download_url',
            'fecha_subida',
        ]

    def get_download_url(self, obj) -> str:
        return f'/api/v1/me/cases/{obj.caso_id}/evidence/{obj.id}/download/'


class CaseEvidenceUpdateSerializer(serializers.ModelSerializer):
    """ADM-11 (AMP-10): PATCH /api/v1/admin/cases/{case_id}/evidence/{evidence_id}/"""

    class Meta:
        model = CaseEvidence
        fields = ['descripcion', 'audiencia', 'estado_revision']


class CaseCorrectionRequestSerializer(serializers.ModelSerializer):
    id_solicitud = serializers.UUIDField(source='id', read_only=True)
    solicitante_nombre = serializers.CharField(source='solicitante.full_name', read_only=True)
    revisor_nombre = serializers.CharField(source='revisor.full_name', read_only=True)

    class Meta:
        model = CaseCorrectionRequest
        fields = [
            'id',
            'id_solicitud',
            'caso',
            'solicitante',
            'solicitante_nombre',
            'motivo',
            'estado',
            'respuesta',
            'revisor',
            'revisor_nombre',
            'fecha_solicitud',
            'fecha_respuesta',
            'fecha_revision',
        ]
        read_only_fields = fields


class CaseContributionSerializer(serializers.ModelSerializer):
    id_aporte = serializers.UUIDField(source='id', read_only=True)
    id_solicitud_correccion = serializers.UUIDField(source='solicitud_correccion_id', required=False, allow_null=True)
    autor_nombre = serializers.CharField(source='usuario.full_name', read_only=True)
    evidencias = CaseEvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = CaseContribution
        fields = [
            'id',
            'id_aporte',
            'caso',
            'usuario',
            'autor_nombre',
            'id_solicitud_correccion',
            'contenido',
            'evidencias',
            'fecha_creacion',
        ]
        read_only_fields = ['id', 'id_aporte', 'caso', 'usuario', 'autor_nombre', 'evidencias', 'fecha_creacion']


class FollowedCaseSerializer(serializers.ModelSerializer):
    id_seguimiento_usuario = serializers.UUIDField(source='id', read_only=True)
    id_caso = serializers.UUIDField(source='caso_id', read_only=True)
    codigo = serializers.CharField(source='caso.codigo', read_only=True)
    titulo = serializers.CharField(source='caso.titulo', read_only=True)

    class Meta:
        model = FollowedCase
        fields = [
            'id',
            'id_seguimiento_usuario',
            'id_caso',
            'codigo',
            'titulo',
            'activo',
            'fecha_creacion',
            'fecha_baja',
        ]
        read_only_fields = fields


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
    tipo_categoria = serializers.CharField(source='tipo_caso.categoria', read_only=True)
    tipo_naturaleza = serializers.CharField(source='tipo_caso.naturaleza', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)
    id_municipio = serializers.UUIDField(source='comunidad.municipio_id', read_only=True)
    municipio_nombre = serializers.CharField(source='comunidad.municipio.nombre', read_only=True)
    id_departamento = serializers.UUIDField(source='comunidad.municipio.departamento_id', read_only=True)
    departamento_nombre = serializers.CharField(source='comunidad.municipio.departamento.nombre', read_only=True)
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
            'tipo_categoria',
            'tipo_naturaleza',
            'comunidad',
            'comunidad_nombre',
            'id_municipio',
            'municipio_nombre',
            'id_departamento',
            'departamento_nombre',
            'estado',
            'estado_nombre',
            'prioridad',
            'estado_publicacion',
            'familias_afectadas',
            'meses_afectacion',
            'public_location',
            'fecha_creacion',
            'fecha_aprobacion',
        ]
        read_only_fields = fields


class PublicCaseDetailSerializer(PublicCaseListSerializer):
    public_updates = serializers.SerializerMethodField()
    public_status_history = serializers.SerializerMethodField()
    approved_comments = serializers.SerializerMethodField()
    public_evidence = serializers.SerializerMethodField()

    class Meta(PublicCaseListSerializer.Meta):
        fields = PublicCaseListSerializer.Meta.fields + [
            'descripcion',
            'resultado_resumen',
            'fecha_resolucion',
            'public_updates',
            'public_status_history',
            'public_evidence',
            'approved_comments',
        ]

    def get_public_updates(self, obj):
        qs = obj.seguimientos.filter(visible_publicamente=True)
        return PublicCaseUpdateSerializer(qs, many=True).data

    def get_public_status_history(self, obj):
        qs = obj.historial_estados.select_related('estado_anterior', 'estado_nuevo').all()
        return PublicCaseStatusHistorySerializer(qs, many=True).data

    def get_public_evidence(self, obj):
        qs = obj.evidencias.filter(
            audiencia=CaseEvidence.Audiencia.PUBLICO,
            estado_revision=CaseEvidence.EstadoRevision.APROBADA,
        )
        return CaseEvidenceSerializer(qs, many=True).data

    def get_approved_comments(self, obj):
        from apps.communications.models import CaseComment
        from apps.communications.serializers import PublicCaseCommentSerializer

        qs = obj.comentarios.filter(estado_moderacion=CaseComment.EstadoModeracion.APROBADO).select_related('usuario')
        return PublicCaseCommentSerializer(qs, many=True).data


class CitizenCaseCreateUpdateSerializer(serializers.ModelSerializer):
    id_caso = serializers.UUIDField(source='id', read_only=True)
    radicado_code = serializers.CharField(source='codigo', read_only=True)
    id_tipo_caso = serializers.PrimaryKeyRelatedField(
        source='tipo_caso',
        queryset=CaseCategory.objects.filter(activo=True),
        required=False,
    )
    category = serializers.PrimaryKeyRelatedField(
        source='tipo_caso',
        queryset=CaseCategory.objects.filter(activo=True),
        required=False,
    )
    id_comunidad = serializers.PrimaryKeyRelatedField(
        source='comunidad',
        queryset=Community.objects.filter(activo=True),
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
    acepta_tratamiento_datos = serializers.BooleanField(required=False, write_only=True, default=True)
    accepts_data_policy = serializers.BooleanField(required=False, write_only=True, default=True)
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    tipo_nombre = serializers.CharField(source='tipo_caso.nombre', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)
    municipio_nombre = serializers.CharField(source='comunidad.municipio.nombre', read_only=True)
    departamento_nombre = serializers.CharField(source='comunidad.municipio.departamento.nombre', read_only=True)
    moderation_status = serializers.CharField(source='estado_publicacion', read_only=True)
    management_status = serializers.CharField(source='estado.nombre', read_only=True)
    active_assignment = CaseAssignmentSerializer(read_only=True)
    active_correction_request = CaseCorrectionRequestSerializer(read_only=True)
    solicitudes_correccion = CaseCorrectionRequestSerializer(many=True, read_only=True)
    aportes = CaseContributionSerializer(many=True, read_only=True)
    seguimientos = serializers.SerializerMethodField()
    evidencias = serializers.SerializerMethodField()
    allowed_actions = serializers.SerializerMethodField()

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
            'id_tipo_caso',
            'tipo_nombre',
            'category',
            'comunidad',
            'id_comunidad',
            'comunidad_nombre',
            'municipio_nombre',
            'departamento_nombre',
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
            'familias_afectadas',
            'meses_afectacion',
            'resultado_resumen',
            'fecha_resolucion',
            'acepta_tratamiento_datos',
            'accepts_data_policy',
            'active_assignment',
            'active_correction_request',
            'solicitudes_correccion',
            'aportes',
            'seguimientos',
            'evidencias',
            'allowed_actions',
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
            'estado_publicacion',
            'moderation_status',
            'resultado_resumen',
            'fecha_resolucion',
            'active_assignment',
            'active_correction_request',
            'solicitudes_correccion',
            'aportes',
            'seguimientos',
            'evidencias',
            'allowed_actions',
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

    def get_seguimientos(self, obj):
        # CIT-05 / AMP-08: El ciudadano solo ve seguimientos con audiencia 'publico' o 'ciudadano', NUNCA 'interno'
        qs = obj.seguimientos.filter(
            audiencia__in=[CaseUpdate.Audiencia.PUBLICO, CaseUpdate.Audiencia.CIUDADANO]
        )
        return CaseUpdateSerializer(qs, many=True).data

    def get_evidencias(self, obj):
        qs = obj.evidencias.exclude(audiencia=CaseEvidence.Audiencia.PRIVADO)
        return CaseEvidenceSerializer(qs, many=True).data

    def get_allowed_actions(self, obj) -> list[str]:
        request = self.context.get('request')
        user = getattr(request, 'user', None) if request else None
        return CaseService.get_allowed_actions(user, obj)

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

            accepted = attrs.get('acepta_tratamiento_datos')
            if accepted is None:
                accepted = attrs.get('accepts_data_policy', True)
            if not accepted:
                raise serializers.ValidationError(
                    {'acepta_tratamiento_datos': 'Debe aceptar la política de tratamiento de datos para radicar el caso.'}
                )

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
    usuario_telefono = serializers.CharField(source='usuario.telefono', read_only=True)
    tipo_nombre = serializers.CharField(source='tipo_caso.nombre', read_only=True)
    tipo_categoria = serializers.CharField(source='tipo_caso.categoria', read_only=True)
    tipo_naturaleza = serializers.CharField(source='tipo_caso.naturaleza', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)
    id_municipio = serializers.UUIDField(source='comunidad.municipio_id', read_only=True)
    municipio_nombre = serializers.CharField(source='comunidad.municipio.nombre', read_only=True)
    id_departamento = serializers.UUIDField(source='comunidad.municipio.departamento_id', read_only=True)
    departamento_nombre = serializers.CharField(source='comunidad.municipio.departamento.nombre', read_only=True)
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    moderation_status = serializers.CharField(source='estado_publicacion', read_only=True)
    management_status = serializers.CharField(source='estado.nombre', read_only=True)
    active_assignment = CaseAssignmentSerializer(read_only=True)
    active_correction_request = CaseCorrectionRequestSerializer(read_only=True)
    solicitudes_correccion = CaseCorrectionRequestSerializer(many=True, read_only=True)
    aportes = CaseContributionSerializer(many=True, read_only=True)
    asignaciones = CaseAssignmentSerializer(many=True, read_only=True)
    seguimientos = CaseUpdateSerializer(many=True, read_only=True)
    historial_estados = CaseStatusHistorySerializer(many=True, read_only=True)
    evidencias = CaseEvidenceSerializer(many=True, read_only=True)
    allowed_actions = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = [
            'id',
            'id_caso',
            'codigo',
            'radicado_code',
            'titulo',
            'descripcion',
            'usuario',
            'usuario_nombre',
            'usuario_correo',
            'usuario_telefono',
            'tipo_caso',
            'tipo_nombre',
            'tipo_categoria',
            'tipo_naturaleza',
            'comunidad',
            'comunidad_nombre',
            'id_municipio',
            'municipio_nombre',
            'id_departamento',
            'departamento_nombre',
            'estado',
            'estado_nombre',
            'management_status',
            'prioridad',
            'estado_publicacion',
            'moderation_status',
            'ubicacion',
            'direccion_referencia',
            'familias_afectadas',
            'meses_afectacion',
            'resultado_resumen',
            'seguimiento_resolucion',
            'usuario_resolucion',
            'fecha_resolucion',
            'active_assignment',
            'active_correction_request',
            'solicitudes_correccion',
            'aportes',
            'asignaciones',
            'seguimientos',
            'historial_estados',
            'evidencias',
            'allowed_actions',
            'fecha_creacion',
            'fecha_actualizacion',
            'fecha_aprobacion',
        ]
        read_only_fields = ['id', 'id_caso', 'codigo', 'usuario', 'fecha_creacion', 'fecha_actualizacion']

    def get_allowed_actions(self, obj) -> list[str]:
        request = self.context.get('request')
        user = getattr(request, 'user', None) if request else None
        return CaseService.get_allowed_actions(user, obj)


class CaseModerationActionSerializer(serializers.Serializer):
    estado_publicacion = serializers.CharField(required=False)
    moderation_status = serializers.CharField(required=False)
    accion = serializers.CharField(required=False)
    solicitar_correccion = serializers.BooleanField(required=False, default=False)
    motivo = serializers.CharField(required=False, allow_blank=True, default='')
    moderation_reason = serializers.CharField(required=False, allow_blank=True, default='')
    prioridad = serializers.CharField(required=False)
    priority = serializers.CharField(required=False)

    def validate(self, attrs):
        pub = (
            attrs.get('estado_publicacion')
            or attrs.get('moderation_status')
            or attrs.get('accion')
        )
        solicitar = attrs.get('solicitar_correccion', False)
        if not pub and not solicitar:
            raise serializers.ValidationError({'estado_publicacion': 'Debe indicar el nuevo estado de publicación o acción.'})
        attrs['resolved_pub'] = pub or 'solicitar_correccion'
        attrs['resolved_solicitar_correccion'] = solicitar or (str(pub).lower() in ('solicitar_correccion', 'correccion_solicitada'))
        attrs['resolved_motivo'] = attrs.get('motivo') or attrs.get('moderation_reason') or ''
        attrs['resolved_prio'] = attrs.get('prioridad') or attrs.get('priority')
        return attrs


class CaseAssignResponsibleSerializer(serializers.Serializer):
    id_responsable = serializers.UUIDField(required=False)
    assigned_to = serializers.UUIDField(required=False)
    motivo = serializers.CharField(required=False, allow_blank=True, default='')

    def validate(self, attrs):
        resp_id = attrs.get('id_responsable') or attrs.get('assigned_to')
        if not resp_id:
            raise serializers.ValidationError({'id_responsable': 'Debe indicar el UUID del responsable.'})
        attrs['resolved_responsable_id'] = resp_id
        return attrs


class CaseManagementStatusSerializer(serializers.Serializer):
    id_estado = serializers.CharField(required=False)
    estado = serializers.CharField(required=False)
    management_status = serializers.CharField(required=False)
    titulo = serializers.CharField(required=False, allow_blank=True, default='')
    descripcion = serializers.CharField(required=False, allow_blank=True, default='')
    motivo = serializers.CharField(required=False, allow_blank=True, default='')
    observations = serializers.CharField(required=False, allow_blank=True, default='')
    final_result = serializers.CharField(required=False, allow_blank=True, default='')
    resultado_resumen = serializers.CharField(required=False, allow_blank=True, default='')

    def validate(self, attrs):
        st = attrs.get('id_estado') or attrs.get('estado') or attrs.get('management_status') or 'resuelto'
        attrs['resolved_status'] = st
        attrs['resolved_resultado'] = (
            attrs.get('resultado_resumen')
            or attrs.get('final_result')
            or ''
        )
        attrs['resolved_motivo'] = (
            attrs.get('motivo')
            or attrs.get('descripcion')
            or attrs['resolved_resultado']
            or attrs.get('observations')
            or ''
        )
        return attrs


class CaseUpdateCreateSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=200, required=False, allow_blank=True)
    title = serializers.CharField(max_length=200, required=False, allow_blank=True)
    descripcion = serializers.CharField(required=False)
    content = serializers.CharField(required=False, allow_blank=True)
    audiencia = serializers.CharField(required=False)
    visibility = serializers.CharField(required=False)
    visible_publicamente = serializers.BooleanField(required=False)
    tipo_evento = serializers.CharField(required=False, default=CaseUpdate.TipoEvento.SEGUIMIENTO)
    id_estado = serializers.CharField(required=False, allow_blank=True)
    estado = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        titulo = (attrs.get('titulo') or attrs.get('title') or '').strip() or None
        desc = attrs.get('descripcion') or attrs.get('content') or ''
        if not desc.strip():
            raise serializers.ValidationError({'descripcion': 'La descripción del seguimiento es obligatoria.'})
        attrs['resolved_titulo'] = titulo
        attrs['resolved_descripcion'] = desc.strip()
        aud = attrs.get('audiencia') or attrs.get('visibility')
        if aud == 'autor':
            aud = CaseUpdate.Audiencia.CIUDADANO
        attrs['resolved_audiencia'] = aud
        attrs['resolved_visible'] = bool(attrs.get('visible_publicamente', False))
        attrs['resolved_new_status'] = attrs.get('id_estado') or attrs.get('estado') or None
        return attrs
