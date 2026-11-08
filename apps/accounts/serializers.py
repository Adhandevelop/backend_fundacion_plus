from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from apps.accounts.models import (
    ResponsibleScopeAssignment,
    Role,
    User,
    normalize_role_name,
)


class RoleSerializer(serializers.ModelSerializer):
    id_rol = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'id_rol', 'nombre', 'descripcion']


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
        comunidad = attrs.get('comunidad')
        tipo_caso = attrs.get('tipo_caso')
        if not comunidad and not tipo_caso:
            raise serializers.ValidationError(
                'Debe especificar al menos una comunidad o un tipo de caso (ck_ambito_responsable).'
            )
        return attrs


class UserMeSerializer(serializers.ModelSerializer):
    id_usuario = serializers.UUIDField(source='id', read_only=True)
    id_rol = serializers.UUIDField(source='rol_id', read_only=True)
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    primary_role = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    full_name = serializers.CharField(read_only=True)
    ambitos_responsable = ResponsibleScopeAssignmentSerializer(
        source='asignaciones_ambito',
        many=True,
        read_only=True,
    )

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
            'ambitos_responsable',
            'fecha_registro',
            'fecha_actualizacion',
        ]
        read_only_fields = [
            'id',
            'id_usuario',
            'id_rol',
            'rol_nombre',
            'correo',
            'estado',
            'primary_role',
            'roles',
            'permissions',
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


class CitizenRegistrationSerializer(serializers.Serializer):
    correo = serializers.EmailField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, min_length=8)
    nombres = serializers.CharField(max_length=100, required=False)
    apellidos = serializers.CharField(max_length=100, required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    telefono = serializers.CharField(max_length=20, required=False, allow_blank=True)
    accepts_data_policy = serializers.BooleanField(default=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_accepts_data_policy(self, value):
        if not value:
            raise serializers.ValidationError(
                'Debe aceptar la política de tratamiento de datos personales (Ley 1581 de 2012).'
            )
        return value

    def validate(self, attrs):
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
        return User.objects.create_user(
            email=validated_data['resolved_correo'],
            password=validated_data['password'],
            nombres=validated_data['resolved_nombres'],
            apellidos=validated_data['resolved_apellidos'],
            telefono=validated_data.get('telefono') or None,
            role_name=Role.Nombre.CIUDADANO,
        )


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


class AdminUserCreateUpdateSerializer(serializers.ModelSerializer):
    id_usuario = serializers.UUIDField(source='id', read_only=True)
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

    def get_primary_role(self, obj):
        return obj.get_primary_role()

    def get_roles(self, obj):
        return obj.get_role_codes()

    @transaction.atomic
    def create(self, validated_data):
        rol_nombre = validated_data.pop('rol_nombre', None)
        rol_obj = validated_data.pop('rol', None)
        password = validated_data.pop('password', None)
        if rol_obj is None:
            target = normalize_role_name(rol_nombre or Role.Nombre.CIUDADANO)
            rol_obj, _ = Role.objects.get_or_create(nombre=target)
        return User.objects.create_user(password=password, rol=rol_obj, **validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        rol_nombre = validated_data.pop('rol_nombre', None)
        password = validated_data.pop('password', None)
        if rol_nombre:
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
    role_code = serializers.CharField()
    motivo = serializers.CharField(required=False, allow_blank=True, default='')
    id_comunidad = serializers.UUIDField(required=False, allow_null=True)
    id_tipo_caso = serializers.UUIDField(required=False, allow_null=True)
