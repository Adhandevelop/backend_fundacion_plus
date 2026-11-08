from rest_framework import serializers
from apps.communications.models import (
    CaseComment,
    CaseMessage,
    EventProposal,
    SiteSetting,
)


class PublicCaseCommentSerializer(serializers.ModelSerializer):
    id_comentario = serializers.UUIDField(source='id', read_only=True)
    autor_nombre = serializers.CharField(source='usuario.full_name', read_only=True)

    class Meta:
        model = CaseComment
        fields = [
            'id',
            'id_comentario',
            'autor_nombre',
            'contenido',
            'fecha_creacion',
        ]
        read_only_fields = fields


class CaseCommentSerializer(serializers.ModelSerializer):
    id_comentario = serializers.UUIDField(source='id', read_only=True)
    autor_nombre = serializers.CharField(source='usuario.full_name', read_only=True)
    caso_codigo = serializers.CharField(source='caso.codigo', read_only=True)
    content = serializers.CharField(source='contenido', required=False)

    class Meta:
        model = CaseComment
        fields = [
            'id',
            'id_comentario',
            'caso',
            'caso_codigo',
            'usuario',
            'autor_nombre',
            'contenido',
            'content',
            'estado_moderacion',
            'fecha_creacion',
        ]
        read_only_fields = [
            'id',
            'id_comentario',
            'caso',
            'caso_codigo',
            'usuario',
            'autor_nombre',
            'estado_moderacion',
            'fecha_creacion',
        ]
        extra_kwargs = {
            'contenido': {'required': False},
        }

    def validate(self, attrs):
        if not attrs.get('contenido'):
            raise serializers.ValidationError({'contenido': 'El contenido del comentario es obligatorio.'})
        return attrs


class CommentModerationActionSerializer(serializers.Serializer):
    estado_moderacion = serializers.CharField(required=False)
    moderation_status = serializers.CharField(required=False)

    def validate(self, attrs):
        raw = (attrs.get('estado_moderacion') or attrs.get('moderation_status') or '').strip().lower()
        mapping = {
            'approved': CaseComment.EstadoModeracion.APROBADO,
            'aprobado': CaseComment.EstadoModeracion.APROBADO,
            'rejected': CaseComment.EstadoModeracion.RECHAZADO,
            'rechazado': CaseComment.EstadoModeracion.RECHAZADO,
            'oculto': CaseComment.EstadoModeracion.OCULTO,
            'hidden': CaseComment.EstadoModeracion.OCULTO,
        }
        if raw not in mapping:
            raise serializers.ValidationError({'estado_moderacion': 'Estado de moderación no válido.'})
        attrs['resolved_status'] = mapping[raw]
        return attrs


class CaseMessageSerializer(serializers.ModelSerializer):
    id_mensaje = serializers.UUIDField(source='id', read_only=True)
    remitente_nombre = serializers.CharField(source='remitente.full_name', read_only=True)
    destinatario_nombre = serializers.CharField(source='destinatario.full_name', read_only=True)
    content = serializers.CharField(source='contenido', required=False)

    class Meta:
        model = CaseMessage
        fields = [
            'id',
            'id_mensaje',
            'caso',
            'remitente',
            'remitente_nombre',
            'destinatario',
            'destinatario_nombre',
            'contenido',
            'content',
            'fecha_envio',
            'fecha_lectura',
        ]
        read_only_fields = [
            'id',
            'id_mensaje',
            'caso',
            'remitente',
            'remitente_nombre',
            'destinatario_nombre',
            'fecha_envio',
            'fecha_lectura',
        ]
        extra_kwargs = {
            'contenido': {'required': False},
            'destinatario': {'required': False},
        }

    def validate(self, attrs):
        if not attrs.get('contenido'):
            raise serializers.ValidationError({'contenido': 'El contenido del mensaje privado es obligatorio.'})
        return attrs


class EventProposalSerializer(serializers.ModelSerializer):
    id_propuesta = serializers.UUIDField(source='id', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)

    class Meta:
        model = EventProposal
        fields = [
            'id',
            'id_propuesta',
            'usuario',
            'comunidad',
            'comunidad_nombre',
            'nombre_contacto',
            'telefono_contacto',
            'comunidad_declarada',
            'acepta_tratamiento_datos',
            'iniciativa_solicitada',
            'iniciativa_generada',
            'titulo',
            'descripcion',
            'tipo_actividad',
            'fecha_sugerida',
            'estado',
            'respuesta',
            'revisor',
            'fecha_creacion',
            'fecha_revision',
        ]
        read_only_fields = [
            'id',
            'id_propuesta',
            'usuario',
            'iniciativa_generada',
            'estado',
            'respuesta',
            'revisor',
            'fecha_creacion',
            'fecha_revision',
        ]

    def validate_acepta_tratamiento_datos(self, value):
        if not value:
            raise serializers.ValidationError(
                'Debe aceptar el tratamiento de datos personales (ck_propuesta_consentimiento).'
            )
        return value


class AdminEventProposalSerializer(EventProposalSerializer):
    class Meta(EventProposalSerializer.Meta):
        read_only_fields = ['id', 'id_propuesta', 'usuario', 'revisor', 'fecha_creacion']


class SiteSettingSerializer(serializers.ModelSerializer):
    id_configuracion = serializers.UUIDField(source='id', read_only=True)
    key = serializers.CharField(source='clave', required=False)
    value = serializers.JSONField(source='valor', required=False)

    class Meta:
        model = SiteSetting
        fields = [
            'id',
            'id_configuracion',
            'clave',
            'key',
            'valor',
            'value',
            'fecha_actualizacion',
        ]
        read_only_fields = ['id', 'id_configuracion', 'fecha_actualizacion']
        extra_kwargs = {
            'clave': {'required': False},
            'valor': {'required': False},
        }
