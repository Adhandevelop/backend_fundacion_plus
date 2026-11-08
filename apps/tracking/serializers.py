from rest_framework import serializers
from apps.tracking.models import CaseStatusHistory, CaseUpdate


class PublicCaseUpdateSerializer(serializers.ModelSerializer):
    id_seguimiento = serializers.UUIDField(source='id', read_only=True)

    class Meta:
        model = CaseUpdate
        fields = [
            'id',
            'id_seguimiento',
            'descripcion',
            'fecha_seguimiento',
            'visible_publicamente',
        ]
        read_only_fields = fields


class CaseUpdateSerializer(serializers.ModelSerializer):
    id_seguimiento = serializers.UUIDField(source='id', read_only=True)
    autor_nombre = serializers.CharField(source='usuario.full_name', read_only=True)

    class Meta:
        model = CaseUpdate
        fields = [
            'id',
            'id_seguimiento',
            'caso',
            'usuario',
            'autor_nombre',
            'descripcion',
            'fecha_seguimiento',
            'visible_publicamente',
        ]
        read_only_fields = ['id', 'id_seguimiento', 'caso', 'usuario', 'autor_nombre', 'fecha_seguimiento']


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
