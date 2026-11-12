import json
import struct
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Optional, Tuple
from django.core.exceptions import ValidationError
from django.db import models
from drf_spectacular.utils import extend_schema_field, inline_serializer
from rest_framework import serializers as drf_serializers
from core.validators import (
    validate_colombia_latitude,
    validate_colombia_longitude,
    validate_geojson_geometry,
)

SRID_WGS84 = 4326


def make_geojson_point(longitude: Optional[ Any], latitude: Optional[Any]) -> Optional[dict]:
    """Builds a standard RFC 7946 GeoJSON Point (SRID 4326) for Leaflet/PostGIS consumption."""
    if longitude is None or latitude is None:
        return None
    return {
        'type': 'Point',
        'srid': SRID_WGS84,
        'coordinates': [float(longitude), float(latitude)],
    }


def obfuscate_coordinates(
    latitude: Any,
    longitude: Any,
    fallback_lat: Optional[Any] = None,
    fallback_lon: Optional[Any] = None,
) -> Tuple[Decimal, Decimal]:
    """
    Generalizes/truncates sensitive coordinates to protect citizen privacy.
    Rounds to 2 decimal places (~1.1 km grid resolution) or uses community centroid.
    """
    if fallback_lat is not None and fallback_lon is not None:
        return Decimal(str(fallback_lat)), Decimal(str(fallback_lon))
    quantizer = Decimal('0.01')
    return (
        Decimal(str(latitude)).quantize(quantizer, rounding=ROUND_HALF_UP),
        Decimal(str(longitude)).quantize(quantizer, rounding=ROUND_HALF_UP),
    )


def parse_bbox(bbox_str: str) -> Optional[Tuple[Decimal, Decimal, Decimal, Decimal]]:
    """
    Parses a bounding box query string 'minLon,minLat,maxLon,maxLat'
    and returns (min_lon, min_lat, max_lon, max_lat).
    """
    if not bbox_str:
        return None
    parts = [p.strip() for p in bbox_str.split(',')]
    if len(parts) != 4:
        raise ValueError('El parámetro bbox debe tener el formato minLon,minLat,maxLon,maxLat.')
    try:
        min_lon, min_lat, max_lon, max_lat = (Decimal(p) for p in parts)
    except Exception as exc:
        raise ValueError('Los valores de bbox deben ser coordenadas numéricas válidas.') from exc
    if min_lon > max_lon or min_lat > max_lat:
        raise ValueError('Los límites mínimos del bbox no pueden ser mayores que los máximos.')
    return min_lon, min_lat, max_lon, max_lat


def ewkb_hex_to_geojson_point(hex_str: str) -> Optional[dict]:
    """
    Decodes a PostGIS EWKB hex string for a 2D Point into a GeoJSON Point dict.
    Also handles EWKT 'SRID=4326;POINT(lon lat)' or JSON strings.
    """
    if not hex_str:
        return None
    if isinstance(hex_str, dict):
        return hex_str
    text = str(hex_str).strip()
    if text.startswith('{'):
        return json.loads(text)
    if 'POINT' in text.upper():
        # Parse EWKT: SRID=4326;POINT(-76.532 3.4516)
        coords_part = text.upper().split('POINT')[-1].strip().lstrip('(').rstrip(')')
        lon_str, lat_str = coords_part.split()[:2]
        return make_geojson_point(float(lon_str), float(lat_str))
    try:
        raw = bytes.fromhex(text)
        byte_order = '<' if raw[0] == 1 else '>'
        geom_type = struct.unpack(f'{byte_order}I', raw[1:5])[0]
        has_srid = bool(geom_type & 0x20000000)
        offset = 9 if has_srid else 5
        lon, lat = struct.unpack(f'{byte_order}dd', raw[offset:offset + 16])
        return make_geojson_point(lon, lat)
    except Exception:
        return None


def point_to_ewkt(value: Any) -> Optional[str]:
    """
    Converts a GeoJSON Point dict {'type': 'Point', 'coordinates': [lon, lat], 'srid': 4326},
    lat/lng dict {'lat': ..., 'lng': ...}, or [lon, lat] tuple into PostGIS EWKT 'SRID=4326;POINT(lon lat)'.
    """
    if value is None or value == '':
        return None
    if isinstance(value, str):
        text = value.strip()
        if text.upper().startswith('SRID='):
            if not text.upper().startswith('SRID=4326;'):
                raise ValidationError('Solo se admite el sistema de coordenadas WGS84 (SRID 4326).')
            return text
        if text.startswith('{'):
            value = json.loads(text)
    if isinstance(value, dict):
        srid = value.get('srid')
        if srid is not None:
            try:
                if int(srid) != SRID_WGS84:
                    raise ValidationError(f'Solo se admite el sistema de referencia espacial WGS84 (SRID {SRID_WGS84}).')
            except (ValueError, TypeError):
                raise ValidationError(f'Valor de SRID inválido: {srid}. Se requiere {SRID_WGS84}.')

        coords = value.get('coordinates')
        if coords and len(coords) >= 2:
            lon, lat = float(coords[0]), float(coords[1])
        elif 'lat' in value and ('lng' in value or 'lon' in value):
            lat = float(value['lat'])
            lon = float(value.get('lng', value.get('lon')))
        elif 'latitude' in value and 'longitude' in value:
            lat = float(value['latitude'])
            lon = float(value['longitude'])
        else:
            return None
    elif isinstance(value, (list, tuple)) and len(value) >= 2:
        lon, lat = float(value[0]), float(value[1])
    else:
        raise ValidationError('Formato de punto geográfico inválido. Use {"type": "Point", "coordinates": [lon, lat], "srid": 4326} o {"lat": ..., "lng": ...}.')

    validate_colombia_longitude(Decimal(str(lon)))
    validate_colombia_latitude(Decimal(str(lat)))
    return f'SRID={SRID_WGS84};POINT({lon:.6f} {lat:.6f})'


@extend_schema_field(
    inline_serializer(
        name='GeoPointDTO',
        fields={
            'type': drf_serializers.CharField(default='Point', help_text='Tipo de geometría GeoJSON ("Point")'),
            'srid': drf_serializers.IntegerField(default=4326, help_text='Identificador de referencia espacial (fijado en 4326 / WGS84)'),
            'coordinates': drf_serializers.ListField(
                child=drf_serializers.FloatField(),
                min_length=2,
                max_length=2,
                help_text='Coordenadas [longitud, latitud] en grados decimales (WGS84, bounds Colombia)',
            ),
        },
    )
)
class GeoPointField(drf_serializers.Field):
    """
    Campo DRF para puntos geográficos PostGIS geometry(Point, 4326).
    - Salida (lectura): RFC 7946 GeoJSON: {"type": "Point", "srid": 4326, "coordinates": [lon, lat]}
    - Entrada (escritura): Acepta GeoJSON estándar, objeto {"lat": ..., "lng": ...}, o arreglo [lon, lat].
    - Validación: Obliga SRID 4326 y valida límites geográficos de Colombia.
    """
    def to_representation(self, value):
        if value is None:
            return None
        if isinstance(value, dict) and 'coordinates' in value:
            return value
        if isinstance(value, str):
            res = ewkb_hex_to_geojson_point(value)
            if res:
                return res
        return value

    def to_internal_value(self, data):
        if data is None or data == '':
            return None
        if isinstance(data, str):
            text = data.strip()
            if text.startswith('{'):
                try:
                    data = json.loads(text)
                except Exception:
                    raise drf_serializers.ValidationError('La cadena JSON de ubicación geográfica no es válida.')
            elif 'POINT' in text.upper():
                if text.upper().startswith('SRID=') and not text.upper().startswith('SRID=4326;'):
                    raise drf_serializers.ValidationError('Solo se admite el sistema de coordenadas WGS84 (SRID 4326).')
                res = ewkb_hex_to_geojson_point(text)
                if not res:
                    raise drf_serializers.ValidationError('Cadena EWKT de punto geográfico inválida.')
                data = res

        srid = 4326
        if isinstance(data, dict):
            if 'srid' in data and data['srid'] is not None:
                try:
                    srid = int(data['srid'])
                except (ValueError, TypeError):
                    raise drf_serializers.ValidationError('El valor de "srid" debe ser numérico (4326).')
                if srid != 4326:
                    raise drf_serializers.ValidationError(f'SRID {srid} no soportado. Se exige SRID 4326 (WGS84).')

            if 'coordinates' in data:
                coords = data['coordinates']
                if not isinstance(coords, (list, tuple)) or len(coords) < 2:
                    raise drf_serializers.ValidationError('El campo "coordinates" debe ser un arreglo [longitud, latitud].')
                lon, lat = coords[0], coords[1]
            elif 'lat' in data and ('lng' in data or 'lon' in data):
                lat = data['lat']
                lon = data.get('lng', data.get('lon'))
            elif 'latitude' in data and 'longitude' in data:
                lat = data['latitude']
                lon = data['longitude']
            else:
                raise drf_serializers.ValidationError(
                    'Formato de ubicación no reconocido. Envíe GeoJSON {"type": "Point", "coordinates": [lon, lat], "srid": 4326} '
                    'o un objeto con {"lat": ..., "lng": ...}.'
                )
        elif isinstance(data, (list, tuple)):
            if len(data) < 2:
                raise drf_serializers.ValidationError('El arreglo de coordenadas debe tener al menos [longitud, latitud].')
            lon, lat = data[0], data[1]
        else:
            raise drf_serializers.ValidationError('Tipo de dato no válido para ubicación geográfica.')

        try:
            lon_f = float(lon)
            lat_f = float(lat)
        except (ValueError, TypeError):
            raise drf_serializers.ValidationError('Las coordenadas de longitud y latitud deben ser números válidos.')

        try:
            validate_colombia_longitude(Decimal(str(lon_f)))
            validate_colombia_latitude(Decimal(str(lat_f)))
        except ValidationError as exc:
            raise drf_serializers.ValidationError(list(exc.messages) if hasattr(exc, 'messages') else str(exc))

        return make_geojson_point(lon_f, lat_f)


class PostGISPointField(models.Field):
    """
    Custom Django field that maps natively to PostGIS `geometry(Point,4326)` in PostgreSQL
    (using EWKT/EWKB) and falls back to TEXT in SQLite so tests run without C++ GDAL DLLs.
    """
    description = 'PostGIS geometry(Point, 4326)'

    def get_internal_type(self):
        return 'TextField'

    def db_type(self, connection):
        if connection.vendor == 'postgresql':
            return 'geometry(Point,4326)'
        return 'TEXT'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return ewkb_hex_to_geojson_point(value)

    def to_python(self, value):
        if value is None or isinstance(value, dict):
            return value
        return ewkb_hex_to_geojson_point(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return point_to_ewkt(value)


class PostGISMultiPolygonField(models.Field):
    """
    Custom Django field that maps to `geometry(MultiPolygon,4326)` in PostgreSQL
    or TEXT in SQLite. Accepts NULL or EWKT/GeoJSON.
    """
    description = 'PostGIS geometry(MultiPolygon, 4326)'

    def get_internal_type(self):
        return 'TextField'

    def db_type(self, connection):
        if connection.vendor == 'postgresql':
            return 'geometry(MultiPolygon,4326)'
        return 'TEXT'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        if isinstance(value, dict):
            return value
        text = str(value).strip()
        if text.startswith('{'):
            try:
                return json.loads(text)
            except Exception:
                return {'ewkt': text}
        return {'ewkb_or_ewkt': text}

    def get_prep_value(self, value):
        if value is None or value == '':
            return None
        if isinstance(value, dict):
            if 'ewkt' in value:
                return value['ewkt']
            validate_geojson_geometry(value)
            return json.dumps(value) if self.model._state.db != 'postgresql' else None
        return str(value)
