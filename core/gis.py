import json
import struct
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Optional, Tuple
from django.core.exceptions import ValidationError
from django.db import models
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
    Converts a GeoJSON Point dict {'type': 'Point', 'coordinates': [lon, lat]}
    or [lon, lat] tuple into PostGIS EWKT 'SRID=4326;POINT(lon lat)'.
    """
    if value is None or value == '':
        return None
    if isinstance(value, str):
        if value.upper().startswith('SRID='):
            return value
        if value.startswith('{'):
            value = json.loads(value)
    if isinstance(value, dict):
        coords = value.get('coordinates')
        if not coords or len(coords) < 2:
            return None
        lon, lat = float(coords[0]), float(coords[1])
    elif isinstance(value, (list, tuple)) and len(value) >= 2:
        lon, lat = float(value[0]), float(value[1])
    else:
        raise ValidationError('Formato de punto geográfico inválido. Use {"type": "Point", "coordinates": [lon, lat]}.')

    validate_colombia_longitude(Decimal(str(lon)))
    validate_colombia_latitude(Decimal(str(lat)))
    return f'SRID={SRID_WGS84};POINT({lon:.6f} {lat:.6f})'


class PostGISPointField(models.Field):
    """
    Custom Django field that maps natively to PostGIS `geometry(Point,4326)` in PostgreSQL
    (using EWKT/EWKB) and falls back to TEXT in SQLite so tests run without C++ GDAL DLLs.
    """
    description = 'PostGIS geometry(Point, 4326)'

    def get_internal_type(self):
        return 'JSONField'

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
        return 'JSONField'

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
