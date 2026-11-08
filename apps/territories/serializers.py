from rest_framework import serializers
from apps.territories.models import Community, Department, Municipality


class CommunitySerializer(serializers.ModelSerializer):
    id_comunidad = serializers.UUIDField(source='id', read_only=True)
    id_municipio = serializers.PrimaryKeyRelatedField(
        source='municipio',
        queryset=Municipality.objects.all(),
        required=False,
    )
    municipio_nombre = serializers.CharField(source='municipio.nombre', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Community
        fields = [
            'id',
            'id_comunidad',
            'municipio',
            'id_municipio',
            'municipio_nombre',
            'nombre',
            'descripcion',
            'tipo',
            'tipo_display',
            'ubicacion',
            'activo',
        ]
        extra_kwargs = {
            'municipio': {'required': False},
        }

    def validate(self, attrs):
        if not attrs.get('municipio') and not self.instance:
            raise serializers.ValidationError({'municipio': 'Debe indicar el municipio (municipio o id_municipio).'})
        return attrs


class MunicipalitySerializer(serializers.ModelSerializer):
    id_municipio = serializers.UUIDField(source='id', read_only=True)
    id_departamento = serializers.PrimaryKeyRelatedField(
        source='departamento',
        queryset=Department.objects.all(),
        required=False,
    )
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    comunidades_count = serializers.IntegerField(source='comunidades.count', read_only=True)

    class Meta:
        model = Municipality
        fields = [
            'id',
            'id_municipio',
            'departamento',
            'id_departamento',
            'departamento_nombre',
            'codigo_dane',
            'nombre',
            'comunidades_count',
        ]
        extra_kwargs = {
            'departamento': {'required': False},
        }

    def validate(self, attrs):
        if not attrs.get('departamento') and not self.instance:
            raise serializers.ValidationError(
                {'departamento': 'Debe indicar el departamento (departamento o id_departamento).'}
            )
        return attrs


class DepartmentSerializer(serializers.ModelSerializer):
    id_departamento = serializers.UUIDField(source='id', read_only=True)
    municipios = MunicipalitySerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = [
            'id',
            'id_departamento',
            'codigo_dane',
            'nombre',
            'municipios',
        ]
