from rest_framework import serializers
from apps.communications.models import (
    CaseComment,
    CaseMessage,
    EventProposal,
    LegalAcceptance,
    LegalDocument,
    NewsletterSubscription,
    SiteSetting,
)
from apps.territories.models import Community


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
    estado_moderacion = serializers.ChoiceField(
        choices=['aprobado', 'rechazado', 'oculto', 'approved', 'rejected', 'hidden'],
        required=False,
        help_text="Acción de moderación sobre el comentario: 'aprobado', 'rechazado' u 'oculto'.",
    )
    moderation_status = serializers.CharField(required=False)
    motivo = serializers.CharField(
        required=False,
        allow_blank=True,
        default='',
        help_text='Motivo de moderación (obligatorio al rechazar u ocultar si la política lo exige; se guarda en auditoria_eventos).',
    )
    moderation_reason = serializers.CharField(required=False, allow_blank=True, default='')

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
        attrs['resolved_motivo'] = (attrs.get('motivo') or attrs.get('moderation_reason') or '').strip()
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
    id_comunidad = serializers.PrimaryKeyRelatedField(
        source='comunidad',
        queryset=Community.objects.filter(activo=True),
        required=False,
        allow_null=True,
    )
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)

    class Meta:
        model = EventProposal
        fields = [
            'id',
            'id_propuesta',
            'usuario',
            'comunidad',
            'id_comunidad',
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

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None) if request else None
        has_auth_user = bool(user and user.is_authenticated)

        if not self.instance:
            if not attrs.get('acepta_tratamiento_datos'):
                raise serializers.ValidationError(
                    {'acepta_tratamiento_datos': 'Debe aceptar el tratamiento de datos personales.'}
                )
            comunidad = attrs.get('comunidad')
            comunidad_dec = (attrs.get('comunidad_declarada') or '').strip()
            if not comunidad and not comunidad_dec:
                raise serializers.ValidationError(
                    {'comunidad': 'Debe indicar una comunidad del catálogo o una comunidad_declarada.'}
                )
            if not has_auth_user:
                nombre = (attrs.get('nombre_contacto') or '').strip()
                telefono = (attrs.get('telefono_contacto') or '').strip()
                if not nombre or not telefono:
                    raise serializers.ValidationError(
                        {'nombre_contacto': 'Nombre y teléfono de contacto son obligatorios para postulaciones públicas.'}
                    )
        return attrs


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


class LegalDocumentSerializer(serializers.ModelSerializer):
    id_documento = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = LegalDocument
        fields = [
            'id',
            'id_documento',
            'tipo',
            'version',
            'titulo',
            'contenido',
            'vigente',
            'fecha_vigencia',
        ]
        read_only_fields = fields


class NewsletterSubscriptionSerializer(serializers.Serializer):
    """PUB-09 (AMP-02): POST /api/v1/public/newsletter-subscriptions/"""
    nombre = serializers.CharField(max_length=150, required=False, allow_blank=True)
    correo = serializers.EmailField(max_length=150, required=False)
    email = serializers.EmailField(max_length=150, required=False)
    acepta_tratamiento_datos = serializers.BooleanField(default=True, required=False)

    def validate(self, attrs):
        correo = (attrs.get('correo') or attrs.get('email') or '').strip().lower()
        if not correo:
            raise serializers.ValidationError({'correo': 'El correo electrónico es obligatorio.'})
        if not attrs.get('acepta_tratamiento_datos', True):
            raise serializers.ValidationError(
                {'acepta_tratamiento_datos': 'Debe aceptar la política de tratamiento de datos para suscribirse.'}
            )
        attrs['resolved_correo'] = correo
        return attrs


class NewsletterTokenActionSerializer(serializers.Serializer):
    """PUB-10 y PUB-11: Confirmación o baja de boletín."""
    token = serializers.CharField(required=False, allow_blank=True)
    correo = serializers.EmailField(required=False)
    email = serializers.EmailField(required=False)
