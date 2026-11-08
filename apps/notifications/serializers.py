from rest_framework import serializers
from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    id_notificacion = serializers.UUIDField(source='id', read_only=True)
    caso_codigo = serializers.CharField(source='caso.codigo', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'id_notificacion',
            'usuario',
            'caso',
            'caso_codigo',
            'titulo',
            'mensaje',
            'tipo',
            'leida',
            'fecha_creacion',
        ]
        read_only_fields = fields
