from django.core.exceptions import PermissionDenied as DjangoPermissionDenied, ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Standardizes error responses for Angular HTTP interceptors:
    {
        "code": "validation_error" | "permission_denied" | "not_found" | "error",
        "message": "Human readable message",
        "errors": { ... }
    }
    """
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            exc = ValidationError(detail=exc.message_dict)
        else:
            exc = ValidationError(detail=exc.messages)
    elif isinstance(exc, DjangoPermissionDenied):
        exc = PermissionDenied(detail=str(exc))

    response = exception_handler(exc, context)
    if response is None:
        return None

    code = 'error'
    message = 'Ha ocurrido un error al procesar la solicitud.'
    errors = response.data

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        code = 'validation_error'
        message = 'Error de validación en los datos enviados.'
    elif response.status_code == status.HTTP_401_UNAUTHORIZED:
        code = 'not_authenticated'
        message = 'Autenticación requerida o credenciales inválidas.'
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        code = 'permission_denied'
        message = 'No tiene permisos suficientes para realizar esta acción.'
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        code = 'not_found'
        message = 'El recurso solicitado no existe o no está disponible.'
    elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        code = 'rate_limit_exceeded'
        message = 'Se ha excedido el límite de peticiones permitidas.'

    if isinstance(response.data, dict) and 'detail' in response.data and len(response.data) == 1:
        message = str(response.data['detail'])

    response.data = {
        'code': code,
        'message': message,
        'errors': errors,
    }
    return response
