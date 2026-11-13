from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from apps.cases.models import CaseEvidence
from apps.tracking.models import CaseStatusHistory, CaseUpdate


class CaseUpdateEvidenceItemSerializer(serializers.ModelSerializer):
    """
    P24: Serializador de evidencia asociada a un seguimiento administrativo o respuesta.
    """
    id_evidencia = serializers.UUIDField(source='id', read_only=True)
    id_seguimiento = serializers.UUIDField(source='seguimiento_id', read_only=True, allow_null=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = CaseEvidence
        fields = [
            'id',
            'id_evidencia',
            'id_seguimiento',
            'nombre_original',
            'descripcion',
            'tipo_archivo',
            'mime_type',
            'tamano_bytes',
            'audiencia',
            'estado_revision',
            'ruta_archivo',
            'download_url',
            'fecha_subida',
        ]
        read_only_fields = fields

    def get_download_url(self, obj) -> str:
        return f'/api/v1/me/cases/{obj.caso_id}/evidence/{obj.id}/download/'


class PublicCaseUpdateSerializer(serializers.ModelSerializer):
    id_seguimiento = serializers.UUIDField(source='id', read_only=True)
    evidencias = serializers.SerializerMethodField()

    class Meta:
        model = CaseUpdate
        fields = [
            'id',
            'id_seguimiento',
            'titulo',
            'descripcion',
            'audiencia',
            'tipo_evento',
            'fecha_seguimiento',
            'visible_publicamente',
            'evidencias',
        ]
        read_only_fields = fields

    @extend_schema_field(CaseUpdateEvidenceItemSerializer(many=True))
    def get_evidencias(self, obj):
        # En tracking público solo evidencias públicas aprobadas (regla P24)
        qs = obj.evidencias.filter(
            audiencia=CaseEvidence.Audiencia.PUBLICO,
            estado_revision=CaseEvidence.EstadoRevision.APROBADA,
        )
        return CaseUpdateEvidenceItemSerializer(qs, many=True, context=self.context).data


class CaseUpdateSerializer(serializers.ModelSerializer):
    id_seguimiento = serializers.UUIDField(source='id', read_only=True)
    autor_nombre = serializers.CharField(source='usuario.full_name', read_only=True)
    evidencias = serializers.SerializerMethodField()

    class Meta:
        model = CaseUpdate
        fields = [
            'id',
            'id_seguimiento',
            'caso',
            'usuario',
            'autor_nombre',
            'titulo',
            'descripcion',
            'audiencia',
            'tipo_evento',
            'fecha_seguimiento',
            'visible_publicamente',
            'evidencias',
        ]
        read_only_fields = ['id', 'id_seguimiento', 'caso', 'usuario', 'autor_nombre', 'fecha_seguimiento', 'evidencias']

    @extend_schema_field(CaseUpdateEvidenceItemSerializer(many=True))
    def get_evidencias(self, obj):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        qs = obj.evidencias.all()

        is_internal = (
            user and (
                getattr(user, 'is_staff', False)
                or getattr(user, 'rol', None) in ('admin', 'responsable', 'moderador')
            )
        )
        if not is_internal:
            if user and user.id == obj.caso.usuario_id:
                # El ciudadano creador del caso ve evidencias públicas o de nivel ciudadano
                qs = qs.filter(audiencia__in=[CaseEvidence.Audiencia.PUBLICO, CaseEvidence.Audiencia.CIUDADANO])
            else:
                # Público general / no autenticado: solo aprobadas y públicas
                qs = qs.filter(
                    audiencia=CaseEvidence.Audiencia.PUBLICO,
                    estado_revision=CaseEvidence.EstadoRevision.APROBADA,
                )

        return CaseUpdateEvidenceItemSerializer(qs, many=True, context=self.context).data


class PublicCaseStatusHistorySerializer(serializers.ModelSerializer):
    id_historial = serializers.UUIDField(source='id', read_only=True)
    estado_anterior_nombre = serializers.CharField(source='estado_anterior.nombre', read_only=True)
    estado_nuevo_nombre = serializers.CharField(source='estado_nuevo.nombre', read_only=True)

    class Meta:
        model = CaseStatusHistory
        fields = [
            'id',
            'id_historial',
            'estado_anterior',
            'estado_anterior_nombre',
            'estado_nuevo',
            'estado_nuevo_nombre',
            'motivo',
            'fecha_cambio',
        ]
        read_only_fields = fields


class CaseStatusHistorySerializer(PublicCaseStatusHistorySerializer):
    usuario_nombre = serializers.CharField(source='usuario.full_name', read_only=True)

    class Meta(PublicCaseStatusHistorySerializer.Meta):
        fields = PublicCaseStatusHistorySerializer.Meta.fields + ['caso', 'usuario', 'usuario_nombre']
        read_only_fields = fields
