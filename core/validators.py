import os
from decimal import Decimal
from django.core.exceptions import ValidationError


# Geographic bounding box for Colombia (WGS84 / SRID 4326)
COLOMBIA_LAT_MIN = Decimal('-4.500000')
COLOMBIA_LAT_MAX = Decimal('13.500000')
COLOMBIA_LON_MIN = Decimal('-82.000000')
COLOMBIA_LON_MAX = Decimal('-66.500000')

ALLOWED_EVIDENCE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.pdf', '.mp4', '.doc', '.docx'}
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_UPLOAD_SIZE_MB = 10


def validate_colombia_latitude(value):
    val = Decimal(str(value))
    if not (COLOMBIA_LAT_MIN <= val <= COLOMBIA_LAT_MAX):
        raise ValidationError(
            f'La latitud ({value}) debe estar dentro del rango geográfico válido '
            f'({COLOMBIA_LAT_MIN} a {COLOMBIA_LAT_MAX} en SRID 4326).'
        )


def validate_colombia_longitude(value):
    val = Decimal(str(value))
    if not (COLOMBIA_LON_MIN <= val <= COLOMBIA_LON_MAX):
        raise ValidationError(
            f'La longitud ({value}) debe estar dentro del rango geográfico válido '
            f'({COLOMBIA_LON_MIN} a {COLOMBIA_LON_MAX} en SRID 4326).'
        )


def validate_geojson_geometry(value):
    """Validates that a JSON dictionary conforms to GeoJSON Point, Polygon, or MultiPolygon."""
    if value is None:
        return
    if not isinstance(value, dict):
        raise ValidationError('La geometría GeoJSON debe ser un objeto JSON válido.')
    geom_type = value.get('type')
    coords = value.get('coordinates')
    if geom_type not in {'Point', 'Polygon', 'MultiPolygon'}:
        raise ValidationError(
            'El tipo de geometría GeoJSON debe ser Point, Polygon o MultiPolygon.'
        )
    if not isinstance(coords, (list, tuple)) or len(coords) == 0:
        raise ValidationError('Las coordenadas GeoJSON no pueden estar vacías.')
    if geom_type == 'Point':
        if len(coords) != 2:
            raise ValidationError('Un GeoJSON Point debe tener exactamente [longitud, latitud].')
        validate_colombia_longitude(coords[0])
        validate_colombia_latitude(coords[1])


def validate_file_safety(uploaded_file):
    """Validates file extension and maximum allowed size."""
    if not uploaded_file:
        return
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in ALLOWED_EVIDENCE_EXTENSIONS:
        raise ValidationError(
            f'Extensión de archivo "{ext}" no permitida. '
            f'Permitidas: {", ".join(sorted(ALLOWED_EVIDENCE_EXTENSIONS))}'
        )
    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if uploaded_file.size > max_bytes:
        raise ValidationError(
            f'El archivo supera el tamaño máximo permitido de {MAX_UPLOAD_SIZE_MB} MB.'
        )


def validate_home_hero_image(uploaded_file, max_size_mb: int = 5):
    """
    Valida que el archivo subido sea una imagen real en formato JPG, PNG o WEBP
    con tamaño menor o igual a max_size_mb (5 MB por defecto).
    Comprueba tanto la extensión como los magic bytes del contenido real.
    """
    if not uploaded_file:
        raise ValidationError('Debe proporcionar un archivo de imagen en el campo "image" o "imagen".')

    name = getattr(uploaded_file, 'name', '') or ''
    ext = os.path.splitext(name)[1].lower()
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    if ext not in allowed_extensions:
        raise ValidationError(
            f'Extensión "{ext}" no permitida para la fotografía de portada. Solo se permiten imágenes JPG, PNG o WEBP.'
        )

    max_bytes = max_size_mb * 1024 * 1024
    file_size = getattr(uploaded_file, 'size', 0)
    if file_size > max_bytes:
        raise ValidationError(
            f'El archivo supera el límite acordado de {max_size_mb} MB (tamaño recibido: {file_size} bytes).'
        )

    # Validar magic bytes leyendo los primeros 16 bytes
    initial_pos = uploaded_file.tell() if hasattr(uploaded_file, 'tell') else 0
    header = uploaded_file.read(16)
    if hasattr(uploaded_file, 'seek'):
        uploaded_file.seek(initial_pos)

    is_jpeg = header.startswith(b'\xff\xd8\xff')
    is_png = header.startswith(b'\x89PNG\r\n\x1a\n')
    is_webp = header.startswith(b'RIFF') and len(header) >= 12 and header[8:12] == b'WEBP'

    if not (is_jpeg or is_png or is_webp):
        raise ValidationError(
            'El contenido binario del archivo no corresponde a una imagen válida en formato JPG, PNG o WEBP.'
        )
