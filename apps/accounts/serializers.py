from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from apps.accounts.models import (
    ResponsibleScopeAssignment,
    Role,
    User,
    UserPreference,
    UserProfile,
    normalize_role_name,
)
from apps.communications.models import LegalAcceptance, NewsletterSubscription


class RoleSerializer(serializers.ModelSerializer):
    id_rol = serializers.UUIDField(source='id', read_only=True)
    assignable = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'id_rol', 'nombre', 'descripcion', 'assignable']

    def get_assignable(self, obj) -> bool:
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser


class ResponsibleScopeAssignmentSerializer(serializers.ModelSerializer):
    id_asignacion = serializers.UUIDField(source='id', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)
    tipo_caso_nombre = serializers.CharField(source='tipo_caso.nombre', read_only=True)

    class Meta:
        model = ResponsibleScopeAssignment
        fields = [
            'id',
            'id_asignacion',
            'usuario',
            'comunidad',
            'comunidad_nombre',
            'tipo_caso',
            'tipo_caso_nombre',
            'fecha_asignacion',
            'activo',
        ]
        read_only_fields = ['id', 'id_asignacion', 'fecha_asignacion']

    def validate(self, attrs):
        comunidad = attrs.get('comunidad', getattr(self.instance, 'comunidad', None))
        tipo_caso = attrs.get('tipo_caso', getattr(self.instance, 'tipo_caso', None))
        if not comunidad and not tipo_caso:
            raise serializers.ValidationError(
                'Debe especificar al menos una comunidad o un tipo de caso (ck_ambito_responsable).'
            )
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    id_perfil = serializers.UUIDField(source='id', read_only=True)
    foto_url = serializers.SerializerMethodField()
    id_departamento = serializers.UUIDField(source='departamento_id', read_only=True)
    id_municipio = serializers.UUIDField(source='municipio_id', read_only=True)
    id_comunidad = serializers.UUIDField(source='comunidad_id', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    municipio_nombre = serializers.CharField(source='municipio.nombre', read_only=True)
    comunidad_nombre = serializers.CharField(source='comunidad.nombre', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id_perfil',
            'ruta_foto',
            'foto_url',
            'id_departamento',
            'departamento_nombre',
            'id_municipio',
            'municipio_nombre',
            'id_comunidad',
            'comunidad_nombre',
            'fecha_actualizacion',
        ]
        read_only_fields = fields

    def get_foto_url(self, obj) -> str | None:
        if not obj.ruta_foto:
            return None
        clean = obj.ruta_foto
        if clean.startswith('/api/v1/public/media/'):
            return clean
        if clean.startswith('/media/'):
            clean = clean[len('/media/'):]
        return f"/api/v1/public/media/{clean.lstrip('/')}"


class UserPreferenceSerializer(serializers.ModelSerializer):
    id_preferencia = serializers.UUIDField(source='id', read_only=True)
    notificar_avance_casos = serializers.BooleanField(
        source='notificar_novedades_casos',
        required=False,
        help_text='Alias de notificar_novedades_casos.',
    )
    recibir_boletin = serializers.BooleanField(
        source='suscrito_boletin',
        required=False,
        help_text='Alias de suscrito_boletin.',
    )

    class Meta:
        model = UserPreference
        fields = [
            'id_preferencia',
            'notificar_novedades_casos',
            'notificar_avance_casos',
            'notificar_mensajes',
            'suscrito_boletin',
            'recibir_boletin',
            'fecha_actualizacion',
        ]
        read_only_fields = ['id_preferencia', 'fecha_actualizacion']

    @transaction.atomic
    def update(self, instance, validated_data):
        boletin_changed = 'suscrito_boletin' in validated_data
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        # Regla 18.4.6 de endpoints.md: sincronizar preferencia de boletín con suscripciones_boletin
        if boletin_changed:
            user = instance.usuario
            if instance.suscrito_boletin:
                acceptance = LegalAcceptance.record(
                    finalidad='suscripcion_boletin',
                    tipo_documento='boletin',
                    usuario=user,
                    correo_declarado=user.correo,
                )
                sub, _ = NewsletterSubscription.objects.get_or_create(
                    correo=user.correo,
                    defaults={
                        'nombre': user.full_name,
                        'usuario': user,
                        'estado': NewsletterSubscription.Estado.CONFIRMADA,
                        'aceptacion_legal': acceptance,
                    },
                )
                if sub.estado != NewsletterSubscription.Estado.CONFIRMADA:
                    sub.estado = NewsletterSubscription.Estado.CONFIRMADA
                    sub.usuario = user
                    sub.aceptacion_legal = acceptance
                    sub.save()
            else:
                NewsletterSubscription.objects.filter(correo__iexact=user.correo).update(
                    estado=NewsletterSubscription.Estado.BAJA,
                )
        return instance


class UserMeSerializer(serializers.ModelSerializer):
    id_usuario = serializers.UUIDField(source='id', read_only=True)
    id_rol = serializers.UUIDField(source='rol_id', read_only=True)
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    primary_role = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    can_manage_homepage = serializers.BooleanField(read_only=True)
    can_manage_forms = serializers.BooleanField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    perfil = serializers.SerializerMethodField()
    preferencias = serializers.SerializerMethodField()
    ambitos_responsable = ResponsibleScopeAssignmentSerializer(
        source='asignaciones_ambito',
        many=True,
        read_only=True,
    )
    # Campos opcionales de residencia para PATCH /me/ (AMP-04)
    id_departamento = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    id_municipio = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    id_comunidad = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id',
            'id_usuario',
            'id_rol',
            'rol_nombre',
            'nombres',
            'apellidos',
            'full_name',
            'correo',
            'telefono',
            'estado',
            'primary_role',
            'roles',
            'permissions',
            'can_manage_homepage',
            'can_manage_forms',
            'perfil',
            'preferencias',
            'ambitos_responsable',
            'id_departamento',
            'id_municipio',
            'id_comunidad',
            'fecha_registro',
            'fecha_actualizacion',
        ]
        read_only_fields = [
            'id',
            'id_usuario',
            'id_rol',
            'rol_nombre',
            'estado',
            'primary_role',
            'roles',
            'permissions',
            'can_manage_homepage',
            'can_manage_forms',
            'perfil',
            'preferencias',
            'ambitos_responsable',
            'fecha_registro',
            'fecha_actualizacion',
        ]

    def get_primary_role(self, obj) -> str:
        return obj.get_primary_role()

    def get_roles(self, obj) -> list[str]:
        return obj.get_role_codes()

    def get_permissions(self, obj) -> dict:
        return obj.get_aggregated_permissions()

    def get_perfil(self, obj) -> dict:
        profile, _ = UserProfile.objects.get_or_create(usuario=obj)
        return UserProfileSerializer(profile).data

    def get_preferencias(self, obj) -> dict:
        prefs, _ = UserPreference.objects.get_or_create(usuario=obj)
        return UserPreferenceSerializer(prefs).data

    def validate_correo(self, value):
        normalized = value.strip().lower()
        if User.objects.filter(correo__iexact=normalized).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('Este correo electrónico ya está registrado por otro usuario.')
        return normalized

    def validate(self, attrs):
        # ME-02: Rechazar intentos de modificar rol o estado desde /me/
        initial = getattr(self, 'initial_data', {}) or {}
        if 'rol' in initial or 'id_rol' in initial or 'estado' in initial:
            raise serializers.ValidationError(
                'No está permitido modificar el rol o el estado de la cuenta desde el perfil propio.'
            )
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        dep_id = validated_data.pop('id_departamento', serializers.empty)
        mun_id = validated_data.pop('id_municipio', serializers.empty)
        com_id = validated_data.pop('id_comunidad', serializers.empty)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if dep_id is not serializers.empty or mun_id is not serializers.empty or com_id is not serializers.empty:
            profile, _ = UserProfile.objects.get_or_create(usuario=instance)
            if dep_id is not serializers.empty:
                profile.departamento_id = dep_id
            if mun_id is not serializers.empty:
                profile.municipio_id = mun_id
            if com_id is not serializers.empty:
                profile.comunidad_id = com_id
            profile.save()
        return instance


class CitizenRegistrationSerializer(serializers.Serializer):
    correo = serializers.EmailField(max_length=150, required=False)
    email = serializers.EmailField(max_length=150, required=False)
    username = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(write_only=True, min_length=8)
    nombres = serializers.CharField(max_length=100, required=False)
    apellidos = serializers.CharField(max_length=100, required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    telefono = serializers.CharField(max_length=20, required=False, allow_blank=True)
    accepts_data_policy = serializers.BooleanField(default=True, required=False)
    acepta_tratamiento_datos = serializers.BooleanField(required=False)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        accepted = attrs.get('acepta_tratamiento_datos')
        if accepted is None:
            accepted = attrs.get('accepts_data_policy', True)
        if not accepted:
            raise serializers.ValidationError(
                {'accepts_data_policy': 'Debe aceptar la política de tratamiento de datos personales (Ley 1581 de 2012).'}
            )

        correo = (attrs.get('correo') or attrs.get('email') or attrs.get('username') or '').strip().lower()
        if not correo:
            raise serializers.ValidationError({'correo': 'El correo electrónico es obligatorio.'})
        if '@' not in correo:
            correo = f'{correo}@plus.org'
        if User.objects.filter(correo__iexact=correo).exists():
            raise serializers.ValidationError({'correo': 'Este correo electrónico ya está registrado.'})
        attrs['resolved_correo'] = correo
        attrs['resolved_nombres'] = attrs.get('nombres') or attrs.get('first_name') or 'Ciudadano'
        attrs['resolved_apellidos'] = attrs.get('apellidos') or attrs.get('last_name') or 'PLUS'
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['resolved_correo'],
            password=validated_data['password'],
            nombres=validated_data['resolved_nombres'],
            apellidos=validated_data['resolved_apellidos'],
            telefono=validated_data.get('telefono') or None,
            role_name=Role.Nombre.CIUDADANO,
        )
        UserProfile.objects.get_or_create(usuario=user)
        UserPreference.objects.get_or_create(usuario=user)
        LegalAcceptance.record(
            finalidad='registro_usuario',
            tipo_documento='tratamiento_datos',
            usuario=user,
            correo_declarado=user.correo,
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Soporta inicio de sesión por correo o username."""
    correo = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = (
            attrs.get('correo')
            or attrs.get('email')
            or attrs.get('username')
            or ''
        ).strip()
        password = attrs.get('password')
        if not identifier or not password:
            raise serializers.ValidationError('Debe proporcionar correo/usuario y contraseña.')

        user_obj = User.objects.filter(correo__iexact=identifier).first()
        if not user_obj and '@' not in identifier:
            user_obj = User.objects.filter(correo__iexact=f'{identifier}@plus.org').first()

        correo_to_auth = user_obj.correo if user_obj else identifier
        user = authenticate(username=correo_to_auth, password=password)
        if not user:
            raise serializers.ValidationError('Credenciales inválidas o cuenta inactiva.')
        if not user.is_active:
            raise serializers.ValidationError('Esta cuenta de usuario no se encuentra activa.')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('La contraseña actual no es correcta.')
        return value

    def validate_new_password(self, value):
        validate_password(value, self.context['request'].user)
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    correo = serializers.EmailField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        correo = (attrs.get('correo') or attrs.get('email') or '').strip().lower()
        if not correo:
            raise serializers.ValidationError({'correo': 'El correo electrónico es obligatorio.'})
        attrs['resolved_correo'] = correo
        return attrs


class PasswordResetValidateSerializer(serializers.Serializer):
    uid = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Identificador base64 del usuario (opcional si token viene en formato <uid>.<token>).',
    )
    token = serializers.CharField(help_text='Token de recuperación o cadena compuesta <uid>.<token>.')

    def validate(self, attrs):
        uid = (attrs.get('uid') or '').strip()
        token = (attrs.get('token') or '').strip()
        if not uid and '.' in token:
            uid, token = token.split('.', 1)
        if not uid or not token:
            raise serializers.ValidationError({'token': 'Debe proporcionar uid y token (o token compuesto <uid>.<token>).'})
        attrs['resolved_uid'] = uid
        attrs['resolved_token'] = token
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Identificador base64 del usuario (opcional si token viene en formato <uid>.<token>).',
    )
    token = serializers.CharField(help_text='Token de recuperación o cadena compuesta <uid>.<token>.')
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8, required=False)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        uid = (attrs.get('uid') or '').strip()
        token = (attrs.get('token') or '').strip()
        if not uid and '.' in token:
            uid, token = token.split('.', 1)
        if not uid or not token:
            raise serializers.ValidationError({'token': 'Debe proporcionar uid y token (o token compuesto <uid>.<token>).'})
        confirm = attrs.get('new_password_confirm')
        if confirm is not None and confirm != attrs.get('new_password'):
            raise serializers.ValidationError({'new_password_confirm': 'Las contraseñas no coinciden.'})
        attrs['resolved_uid'] = uid
        attrs['resolved_token'] = token
        return attrs


class AdminUserCreateUpdateSerializer(serializers.ModelSerializer):
    id_usuario = serializers.UUIDField(source='id', read_only=True)
    id_rol = serializers.UUIDField(source='rol_id', required=False)
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    rol_nombre = serializers.CharField(write_only=True, required=False)
    primary_role = serializers.SerializerMethodField(read_only=True)
    roles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'id_usuario',
            'rol',
            'id_rol',
            'rol_nombre',
            'nombres',
            'apellidos',
            'correo',
            'password',
            'telefono',
            'estado',
            'primary_role',
            'roles',
            'fecha_registro',
            'fecha_actualizacion',
        ]
        read_only_fields = ['id', 'id_usuario', 'primary_role', 'roles', 'fecha_registro', 'fecha_actualizacion']
        extra_kwargs = {
            'rol': {'required': False},
        }

    def get_primary_role(self, obj) -> str:
        return obj.get_primary_role()

    def get_roles(self, obj) -> list[str]:
        return obj.get_role_codes()

    def validate_correo(self, value):
        normalized = value.strip().lower()
        qs = User.objects.filter(correo__iexact=normalized)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Este correo electrónico ya está registrado.')
        return normalized

    @transaction.atomic
    def create(self, validated_data):
        rol_nombre = validated_data.pop('rol_nombre', None)
        rol_id = validated_data.pop('rol_id', None)
        rol_obj = validated_data.pop('rol', None)
        password = validated_data.pop('password', None)
        if rol_obj is None and rol_id:
            rol_obj = Role.objects.filter(pk=rol_id).first()
        if rol_obj is None:
            target = normalize_role_name(rol_nombre or Role.Nombre.CIUDADANO)
            rol_obj, _ = Role.objects.get_or_create(nombre=target)
        user = User.objects.create_user(password=password, rol=rol_obj, **validated_data)
        UserProfile.objects.get_or_create(usuario=user)
        UserPreference.objects.get_or_create(usuario=user)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        rol_nombre = validated_data.pop('rol_nombre', None)
        rol_id = validated_data.pop('rol_id', None)
        password = validated_data.pop('password', None)
        if rol_id:
            rol_obj = Role.objects.filter(pk=rol_id).first()
            if rol_obj:
                instance.rol = rol_obj
        elif rol_nombre:
            target = normalize_role_name(rol_nombre)
            rol_obj, _ = Role.objects.get_or_create(nombre=target)
            instance.rol = rol_obj
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AssignUserRoleSerializer(serializers.Serializer):
    """USR-05: Soporta PUT /admin/users/{id}/role/ con un único rol (id_rol UUID o role_code)."""
    id_rol = serializers.UUIDField(required=False)
    role_code = serializers.CharField(required=False)
    rol = serializers.CharField(required=False)
    motivo = serializers.CharField(required=False, allow_blank=True, default='')
    id_comunidad = serializers.UUIDField(required=False, allow_null=True)
    id_tipo_caso = serializers.UUIDField(required=False, allow_null=True)

    def validate(self, attrs):
        id_rol = attrs.get('id_rol')
        role_code = attrs.get('role_code') or attrs.get('rol')
        if not id_rol and not role_code:
            raise serializers.ValidationError('Debe especificar id_rol (UUID) o role_code (nombre del rol único).')
        return attrs


class AdminUserStatusSerializer(serializers.Serializer):
    """USR-06: PATCH /admin/users/{id}/status/ con estado de tres valores."""
    estado = serializers.ChoiceField(choices=User.Estado.choices)
    motivo = serializers.CharField(required=False, allow_blank=True, default='')
