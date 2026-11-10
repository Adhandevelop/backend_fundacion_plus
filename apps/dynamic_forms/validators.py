import re
import uuid
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from rest_framework.exceptions import ValidationError

CODIGO_PREGUNTA_REGEX = re.compile(r'^[a-z0-9_]{2,50}$')


def validate_pregunta_codigo(codigo: str) -> str:
    cleaned = (codigo or '').strip().lower()
    if not CODIGO_PREGUNTA_REGEX.match(cleaned):
        raise ValidationError(
            f'El código "{codigo}" es inválido. Debe contener únicamente minúsculas, números o guiones bajos '
            f'y tener entre 2 y 50 caracteres (ej. "barrio_residencia", "p1_sector").'
        )
    return cleaned


def validate_configuracion_validacion(config: dict) -> dict:
    if not isinstance(config, dict):
        raise ValidationError('La configuración de validación debe ser un objeto JSON.')

    allowed_keys = {
        'min_length', 'max_length',
        'min_value', 'max_value', 'integer_only',
        'min_date', 'max_date',
        'min_items', 'max_items',
        'regex_pattern', 'regex_error_message',
    }
    unknown_keys = set(config.keys()) - allowed_keys
    if unknown_keys:
        raise ValidationError(f'Propiedades de validación no reconocidas: {", ".join(sorted(unknown_keys))}')

    if 'regex_pattern' in config and config['regex_pattern']:
        try:
            re.compile(config['regex_pattern'])
        except re.error as e:
            raise ValidationError(f'El patrón regex configurado no es válido: {e}')

    return config


def validate_idempotency_key(key_str: str) -> uuid.UUID:
    if not key_str:
        raise ValidationError('La cabecera "Idempotency-Key" es obligatoria para enviar el formulario.')
    try:
        return uuid.UUID(str(key_str).strip())
    except (ValueError, AttributeError):
        raise ValidationError('La cabecera "Idempotency-Key" debe ser un UUID válido (ej. 82dc7667-0c15-4fa7-8db1-54b3874b335a).')


def validate_respuesta_contra_pregunta(pregunta, payload: dict) -> dict:
    """
    Valida rigurosamente la respuesta suministrada para una pregunta según su tipo y reglas.
    Retorna un diccionario con los campos tipados listos para guardar en FormularioRespuesta.
    """
    tipo = pregunta.tipo_campo
    config = pregunta.configuracion_validacion or {}
    es_obligatorio = pregunta.es_obligatorio

    result = {
        'valor_texto': None,
        'valor_numero': None,
        'valor_fecha': None,
        'valor_booleano': None,
        'valores_seleccionados': [],
    }

    # Extraer campos posibles
    raw_texto = payload.get('valor_texto')
    raw_numero = payload.get('valor_numero')
    raw_fecha = payload.get('valor_fecha')
    raw_booleano = payload.get('valor_booleano')
    raw_sel_unica = payload.get('valor_seleccionado')
    raw_sel_mult = payload.get('valores_seleccionados')

    if tipo in (pregunta.TipoCampo.TEXTO_CORTO, pregunta.TipoCampo.TEXTO_LARGO):
        if raw_texto is not None:
            raw_texto = str(raw_texto).strip()
        if not raw_texto:
            if es_obligatorio:
                raise ValidationError(f'La pregunta "{pregunta.enunciado}" es obligatoria.')
            return result

        min_len = config.get('min_length')
        max_len = config.get('max_length') or (255 if tipo == pregunta.TipoCampo.TEXTO_CORTO else 4000)

        if min_len and len(raw_texto) < int(min_len):
            raise ValidationError(f'La respuesta a "{pregunta.enunciado}" debe tener mínimo {min_len} caracteres.')
        if max_len and len(raw_texto) > int(max_len):
            raise ValidationError(f'La respuesta a "{pregunta.enunciado}" supera el máximo de {max_len} caracteres.')

        regex = config.get('regex_pattern')
        if regex:
            compiled = re.compile(regex)
            if not compiled.match(raw_texto):
                msg = config.get('regex_error_message') or f'El formato de respuesta para "{pregunta.enunciado}" es inválido.'
                raise ValidationError(msg)

        result['valor_texto'] = raw_texto

    elif tipo == pregunta.TipoCampo.NUMERO:
        if raw_numero is None or raw_numero == '':
            if es_obligatorio:
                raise ValidationError(f'La pregunta "{pregunta.enunciado}" es obligatoria.')
            return result

        try:
            num = Decimal(str(raw_numero))
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError(f'El valor "{raw_numero}" para "{pregunta.enunciado}" debe ser numérico.')

        if config.get('integer_only') and num % 1 != 0:
            raise ValidationError(f'La pregunta "{pregunta.enunciado}" solo admite números enteros.')

        min_val = config.get('min_value')
        max_val = config.get('max_value')
        if min_val is not None and num < Decimal(str(min_val)):
            raise ValidationError(f'El valor para "{pregunta.enunciado}" debe ser mayor o igual a {min_val}.')
        if max_val is not None and num > Decimal(str(max_val)):
            raise ValidationError(f'El valor para "{pregunta.enunciado}" debe ser menor o igual a {max_val}.')

        result['valor_numero'] = num

    elif tipo == pregunta.TipoCampo.FECHA:
        if not raw_fecha:
            if es_obligatorio:
                raise ValidationError(f'La pregunta "{pregunta.enunciado}" es obligatoria.')
            return result

        try:
            parsed_date = datetime.strptime(str(raw_fecha).strip(), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            raise ValidationError(f'La fecha para "{pregunta.enunciado}" debe tener formato YYYY-MM-DD.')

        min_date = config.get('min_date')
        max_date = config.get('max_date')
        if min_date:
            min_d = datetime.strptime(str(min_date).strip(), '%Y-%m-%d').date()
            if parsed_date < min_d:
                raise ValidationError(f'La fecha para "{pregunta.enunciado}" no puede ser anterior a {min_date}.')
        if max_date:
            max_d = datetime.strptime(str(max_date).strip(), '%Y-%m-%d').date()
            if parsed_date > max_d:
                raise ValidationError(f'La fecha para "{pregunta.enunciado}" no puede ser posterior a {max_date}.')

        result['valor_fecha'] = parsed_date

    elif tipo == pregunta.TipoCampo.BOOLEANO:
        if raw_booleano is None:
            if es_obligatorio:
                raise ValidationError(f'La pregunta "{pregunta.enunciado}" es obligatoria.')
            return result

        if not isinstance(raw_booleano, bool):
            if str(raw_booleano).lower() in ('true', '1'):
                raw_booleano = True
            elif str(raw_booleano).lower() in ('false', '0'):
                raw_booleano = False
            else:
                raise ValidationError(f'El valor para "{pregunta.enunciado}" debe ser booleano (true/false).')

        result['valor_booleano'] = raw_booleano

    elif tipo == pregunta.TipoCampo.SELECCION_UNICA:
        if not raw_sel_unica:
            if es_obligatorio:
                raise ValidationError(f'La pregunta "{pregunta.enunciado}" es obligatoria.')
            return result

        val = str(raw_sel_unica).strip()
        opciones_validas = {op.valor for op in pregunta.opciones.all()}
        if val not in opciones_validas:
            raise ValidationError(
                f'La opción seleccionada "{val}" no es válida para la pregunta "{pregunta.enunciado}".'
            )

        result['valor_texto'] = val
        result['valores_seleccionados'] = [val]

    elif tipo == pregunta.TipoCampo.SELECCION_MULTIPLE:
        if raw_sel_mult is None or (isinstance(raw_sel_mult, list) and len(raw_sel_mult) == 0):
            if es_obligatorio:
                raise ValidationError(f'Debe seleccionar al menos una opción para "{pregunta.enunciado}".')
            return result

        if not isinstance(raw_sel_mult, list):
            raise ValidationError(f'Las respuestas para "{pregunta.enunciado}" deben enviarse como una lista.')

        clean_vals = [str(v).strip() for v in raw_sel_mult if str(v).strip()]
        opciones_validas = {op.valor for op in pregunta.opciones.all()}
        invalidas = set(clean_vals) - opciones_validas
        if invalidas:
            raise ValidationError(
                f'Las siguientes opciones seleccionadas no son válidas para "{pregunta.enunciado}": {", ".join(invalidas)}'
            )

        min_items = config.get('min_items')
        max_items = config.get('max_items')
        if min_items and len(clean_vals) < int(min_items):
            raise ValidationError(f'Debe seleccionar al menos {min_items} opciones para "{pregunta.enunciado}".')
        if max_items and len(clean_vals) > int(max_items):
            raise ValidationError(f'Puede seleccionar máximo {max_items} opciones para "{pregunta.enunciado}".')

        result['valores_seleccionados'] = clean_vals

    return result
