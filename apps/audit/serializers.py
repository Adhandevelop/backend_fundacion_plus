from rest_framework import serializers
from apps.audit.models import (
    AuditAccess,
    AuditCase,
    AuditLog,
    AuditPermission,
    AuditSecurity,
)


class AuditLogSerializer(serializers.ModelSerializer):
    id_auditoria = serializers.UUIDField(source='id', read_only=True)
    usuario_correo = serializers.CharField(source='usuario.correo', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id',
            'id_auditoria',
            'usuario',
            'usuario_correo',
            'accion',
            'modulo',
            'tabla_afectada',
            'id_registro',
            'datos_anteriores',
            'datos_nuevos',
            'direccion_ip',
            'user_agent',
            'fecha_evento',
            'resultado',
        ]
        read_only_fields = fields


class AuditAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditAccess
        fields = '__all__'
        read_only_fields = [f.name for f in AuditAccess._meta.fields]


class AuditCaseSerializer(serializers.ModelSerializer):
    caso_codigo = serializers.CharField(source='caso.codigo', read_only=True)

    class Meta:
        model = AuditCase
        fields = [
            'id',
            'caso',
            'caso_codigo',
            'usuario',
            'tipo_accion',
            'estado_anterior',
            'estado_nuevo',
            'motivo',
            'fecha_accion',
        ]
        read_only_fields = fields


class AuditPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditPermission
        fields = '__all__'
        read_only_fields = [f.name for f in AuditPermission._meta.fields]


class AuditSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditSecurity
        fields = '__all__'
        read_only_fields = [f.name for f in AuditSecurity._meta.fields]
