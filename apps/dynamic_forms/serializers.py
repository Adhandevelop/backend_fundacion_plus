from rest_framework import serializers
from apps.dynamic_forms.models import (
    Formulario,
    FormularioEnvio,
    FormularioNotificacion,
    FormularioOpcion,
    FormularioPregunta,
    FormularioRespuesta,
    FormularioToken,
    FormularioVersion,
)
from apps.dynamic_forms.validators import (
    validate_configuracion_validacion,
    validate_pregunta_codigo,
)


class FormularioOpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormularioOpcion
        fields = ['id', 'valor', 'etiqueta', 'orden']


class FormularioPreguntaSerializer(serializers.ModelSerializer):
    opciones = FormularioOpcionSerializer(many=True, required=False)

    class Meta:
        model = FormularioPregunta
        fields = [
            'id',
            'codigo',
            'enunciado',
            'descripcion_ayuda',
            'tipo_campo',
            'es_obligatorio',
            'orden',
            'configuracion_validacion',
            'opciones',
        ]

    def validate_codigo(self, value):
        return validate_pregunta_codigo(value)

    def validate_configuracion_validacion(self, value):
        return validate_configuracion_validacion(value or {})


class FormularioVersionDetailSerializer(serializers.ModelSerializer):
    preguntas = FormularioPreguntaSerializer(many=True, read_only=True)

    class Meta:
        model = FormularioVersion
        fields = [
            'id',
            'numero_version',
            'es_vigente',
            'titulo_congelado',
            'descripcion_congelada',
            'requiere_documento',
            'permite_multiples_envios',
            'publicado_en',
            'preguntas',
        ]


class AdminFormularioListSerializer(serializers.ModelSerializer):
    total_envios = serializers.SerializerMethodField()
    total_versiones = serializers.SerializerMethodField()

    class Meta:
        model = Formulario
        fields = [
            'id',
            'slug',
            'titulo',
            'estado',
            'numero_version_publicada',
            'revision_edicion',
            'total_versiones',
            'total_envios',
            'permite_multiples_envios',
            'requiere_documento',
            'fecha_creacion',
            'fecha_actualizacion',
        ]

    def get_total_envios(self, obj) -> int:
        return obj.envios.count()

    def get_total_versiones(self, obj) -> int:
        return obj.versiones.count()


class AdminFormularioDetailSerializer(serializers.ModelSerializer):
    preguntas_borrador = FormularioPreguntaSerializer(many=True, read_only=True)
    versiones = serializers.SerializerMethodField()
    total_envios = serializers.SerializerMethodField()

    class Meta:
        model = Formulario
        fields = [
            'id',
            'slug',
            'titulo',
            'descripcion',
            'estado',
            'requiere_documento',
            'permite_multiples_envios',
            'numero_version_publicada',
            'revision_edicion',
            'total_envios',
            'fecha_creacion',
            'fecha_actualizacion',
            'preguntas_borrador',
            'versiones',
        ]

    def get_total_envios(self, obj) -> int:
        return obj.envios.count()

    def get_versiones(self, obj) -> list:
        return [
            {
                'id': v.id,
                'numero_version': v.numero_version,
                'es_vigente': v.es_vigente,
                'publicado_en': v.publicado_en,
                'total_envios': v.envios.count(),
                'total_preguntas': v.preguntas.count(),
            }
            for v in obj.versiones.all().order_by('-numero_version')
        ]


class AdminFormularioCreateUpdateSerializer(serializers.ModelSerializer):
    preguntas = FormularioPreguntaSerializer(many=True, required=False)
    revision_esperada = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Formulario
        fields = [
            'id',
            'slug',
            'titulo',
            'descripcion',
            'estado',
            'requiere_documento',
            'permite_multiples_envios',
            'numero_version_publicada',
            'revision_edicion',
            'revision_esperada',
            'preguntas',
        ]
        read_only_fields = ['id', 'estado', 'numero_version_publicada', 'revision_edicion']

    def create(self, validated_data):
        from apps.dynamic_forms.services import FormularioService
        preguntas = validated_data.pop('preguntas', [])
        validated_data.pop('revision_esperada', None)
        formulario = Formulario.objects.create(**validated_data)
        if preguntas:
            FormularioService._sync_draft_questions(formulario, preguntas)
        return formulario

    def update(self, instance, validated_data):
        from apps.dynamic_forms.services import FormularioService
        preguntas = validated_data.pop('preguntas', None)
        request = self.context.get('request')
        actor = request.user if request else None
        data = dict(validated_data)
        if preguntas is not None:
            data['preguntas'] = preguntas
        return FormularioService.save_draft(instance, data, actor=actor)


# ---- Respuestas y Envíos (Admin) ----

class AdminFormularioSubmissionListSerializer(serializers.ModelSerializer):
    numero_version = serializers.IntegerField(source='version.numero_version', read_only=True)
    ciudadano = serializers.SerializerMethodField()

    class Meta:
        model = FormularioEnvio
        fields = [
            'id',
            'numero_version',
            'fecha_envio',
            'estado_vinculacion',
            'ciudadano',
            'usuario_id',
        ]

    def get_ciudadano(self, obj) -> dict:
        def mask_email(email):
            if not email or '@' not in str(email):
                return str(email or '')
            parts = str(email).split('@')
            user_part = parts[0]
            masked_user = (user_part[:2] + '*' * max(1, len(user_part) - 4) + user_part[-2:]) if len(user_part) > 4 else (user_part[:1] + '***')
            return f'{masked_user}@{parts[1]}'

        def mask_doc(doc, tipo):
            if not doc:
                return None
            clean_doc = str(doc).strip()
            if not clean_doc:
                return None
            masked = f'***{clean_doc[-4:]}' if len(clean_doc) >= 4 else '***'
            tipo_prefix = f'{tipo} ' if tipo else ''
            return f'{tipo_prefix}{masked}'.strip()

        def mask_phone(phone):
            if not phone:
                return '***'
            clean_phone = str(phone).strip()
            if not clean_phone:
                return '***'
            if len(clean_phone) >= 7:
                return f'{clean_phone[:3]}****{clean_phone[-3:]}'
            return '***'

        return {
            'nombres': obj.nombres_declarados or '',
            'apellidos': obj.apellidos_declarados or '',
            'correo_enmascarado': mask_email(obj.correo_declarado),
            'telefono_enmascarado': mask_phone(obj.telefono_declarado),
            'documento_enmascarado': mask_doc(obj.numero_documento_declarado, obj.tipo_documento_declarado),
        }


class FormularioRespuestaDetailSerializer(serializers.ModelSerializer):
    valor = serializers.SerializerMethodField()

    class Meta:
        model = FormularioRespuesta
        fields = [
            'id',
            'codigo_pregunta',
            'enunciado_congelado',
            'tipo_campo_congelado',
            'valor',
        ]

    def get_valor(self, obj):
        tipo = obj.tipo_campo_congelado
        if tipo in ('texto_corto', 'texto_largo'):
            return obj.valor_texto
        elif tipo == 'numero':
            return float(obj.valor_numero) if obj.valor_numero is not None else None
        elif tipo == 'fecha':
            return str(obj.valor_fecha) if obj.valor_fecha else None
        elif tipo == 'booleano':
            return obj.valor_booleano
        elif tipo == 'seleccion_unica':
            return obj.valor_texto
        elif tipo == 'seleccion_multiple':
            return obj.valores_seleccionados
        return obj.valor_texto or obj.valores_seleccionados


class AdminFormularioSubmissionDetailSerializer(serializers.ModelSerializer):
    numero_version = serializers.IntegerField(source='version.numero_version', read_only=True)
    formulario = serializers.SerializerMethodField()
    datos_identificacion_completos = serializers.SerializerMethodField()
    aceptacion_legal = serializers.SerializerMethodField()
    respuestas = FormularioRespuestaDetailSerializer(many=True, read_only=True)

    class Meta:
        model = FormularioEnvio
        fields = [
            'id',
            'formulario',
            'numero_version',
            'fecha_envio',
            'estado_vinculacion',
            'datos_identificacion_completos',
            'ip_origen',
            'user_agent',
            'aceptacion_legal',
            'respuestas',
        ]

    def get_formulario(self, obj) -> dict:
        return {
            'id': obj.formulario.id,
            'slug': obj.formulario.slug,
            'titulo': obj.formulario.titulo,
        }

    def get_datos_identificacion_completos(self, obj) -> dict:
        return {
            'nombres': obj.nombres_declarados,
            'apellidos': obj.apellidos_declarados,
            'correo': obj.correo_declarado,
            'telefono': obj.telefono_declarado,
            'tipo_documento': obj.tipo_documento_declarado,
            'numero_documento': obj.numero_documento_declarado,
        }

    def get_aceptacion_legal(self, obj) -> dict | None:
        if not obj.aceptacion_legal:
            return None
        return {
            'version_politica': obj.aceptacion_legal.version_documento,
            'fecha_aceptacion': obj.aceptacion_legal.fecha_aceptacion,
        }


# ---- Público ----

class PublicFormularioDetailSerializer(serializers.ModelSerializer):
    version_activa = serializers.SerializerMethodField()
    politica_datos = serializers.SerializerMethodField()

    class Meta:
        model = Formulario
        fields = [
            'id',
            'slug',
            'titulo',
            'descripcion',
            'estado',
            'requiere_documento',
            'permite_multiples_envios',
            'version_activa',
            'politica_datos',
        ]

    def get_version_activa(self, obj) -> dict | None:
        v = obj.versiones.filter(es_vigente=True).first()
        if not v:
            return None
        return {
            'numero_version': v.numero_version,
            'preguntas': FormularioPreguntaSerializer(v.preguntas.all(), many=True).data,
        }

    def get_politica_datos(self, obj) -> dict | None:
        from apps.communications.models import LegalDocument
        doc = LegalDocument.get_current('tratamiento_datos')
        if not doc:
            return None
        return {
            'id_documento': doc.id,
            'version': doc.version,
            'titulo': doc.titulo,
            'resumen': getattr(doc, 'resumen', None) or doc.contenido[:200] or 'Autorizo a la Corporación PLUS el tratamiento de mis datos personales.',
            'url_contenido': '/api/v1/public/legal/tratamiento_datos/',
        }


class DatosIdentificacionSerializer(serializers.Serializer):
    nombres = serializers.CharField(max_length=150)
    apellidos = serializers.CharField(max_length=150)
    correo = serializers.EmailField(max_length=254)
    telefono = serializers.CharField(max_length=30, required=False, allow_blank=True)
    tipo_documento = serializers.CharField(max_length=20, required=False, allow_blank=True)
    numero_documento = serializers.CharField(max_length=50, required=False, allow_blank=True)


class PublicRespuestaItemSerializer(serializers.Serializer):
    id_pregunta = serializers.UUIDField()
    valor_texto = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    valor_numero = serializers.DecimalField(max_digits=16, decimal_places=4, required=False, allow_null=True)
    valor_fecha = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    valor_booleano = serializers.BooleanField(required=False, allow_null=True)
    valor_seleccionado = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    valores_seleccionados = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
    )


class PublicFormularioSubmitSerializer(serializers.Serializer):
    datos_identificacion = DatosIdentificacionSerializer()
    acepta_politica_datos = serializers.BooleanField()
    id_documento_legal = serializers.UUIDField()
    respuestas = PublicRespuestaItemSerializer(many=True)

    def validate_acepta_politica_datos(self, value):
        if not value:
            raise serializers.ValidationError('Debe aceptar la política de tratamiento de datos personales para continuar.')
        return value


class PublicActivationVerifySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128)
    nueva_contrasena = serializers.CharField(min_length=8, write_only=True)


class PublicActivationResendSerializer(serializers.Serializer):
    correo = serializers.EmailField(max_length=254)


# ---- Ciudadano (“Mis Formularios”) ----

class CitizenSubmissionListSerializer(serializers.ModelSerializer):
    formulario = serializers.SerializerMethodField()
    numero_version = serializers.IntegerField(source='version.numero_version', read_only=True)
    total_respuestas = serializers.SerializerMethodField()

    class Meta:
        model = FormularioEnvio
        fields = [
            'id',
            'formulario',
            'numero_version',
            'fecha_envio',
            'estado_vinculacion',
            'total_respuestas',
        ]

    def get_formulario(self, obj) -> dict:
        return {
            'slug': obj.formulario.slug,
            'titulo': obj.formulario.titulo,
        }

    def get_total_respuestas(self, obj) -> int:
        return obj.respuestas.count()


class CitizenSubmissionDetailSerializer(serializers.ModelSerializer):
    formulario_titulo = serializers.CharField(source='formulario.titulo', read_only=True)
    numero_version = serializers.IntegerField(source='version.numero_version', read_only=True)
    respuestas = FormularioRespuestaDetailSerializer(many=True, read_only=True)

    class Meta:
        model = FormularioEnvio
        fields = [
            'id',
            'formulario_titulo',
            'numero_version',
            'fecha_envio',
            'respuestas',
        ]
