import threading
import uuid
from typing import Any, Dict, Optional
from django.db import connection
from apps.audit.models import (
    AuditAccess,
    AuditCase,
    AuditLog,
    AuditPermission,
    AuditSecurity,
)

_request_context = threading.local()


def set_current_request_meta(ip_address: Optional[str], user_agent: str, user=None):
    _request_context.ip_address = ip_address
    _request_context.user_agent = user_agent or ''
    _request_context.user = user


def get_current_request_meta():
    return (
        getattr(_request_context, 'ip_address', None),
        getattr(_request_context, 'user_agent', ''),
        getattr(_request_context, 'user', None),
    )


class AuditService:
    """
    Servicio central de auditoría para las 5 tablas especializadas de `plus`:
    auditoria_eventos, auditoria_accesos, auditoria_casos, auditoria_permisos, auditoria_seguridad.
    Sincroniza además `SET LOCAL plus.actor_id` cuando se ejecuta en PostgreSQL.
    """

    @staticmethod
    def set_db_actor_session(actor):
        if not actor or not getattr(actor, 'is_authenticated', False):
            return
        if connection.vendor == 'postgresql':
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT set_config('plus.actor_id', %s, true);", [str(actor.pk)])
            except Exception:
                pass

    @staticmethod
    def _extract_meta(request=None, actor=None):
        ip_address, user_agent, ctx_user = get_current_request_meta()
        if request is not None:
            xff = request.META.get('HTTP_X_FORWARDED_FOR')
            ip_address = xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            if actor is None and getattr(request, 'user', None) and request.user.is_authenticated:
                actor = request.user
        elif actor is None and ctx_user and getattr(ctx_user, 'is_authenticated', False):
            actor = ctx_user
        if actor and not getattr(actor, 'is_authenticated', False):
            actor = None
        return ip_address, user_agent, actor

    @classmethod
    def log(
        cls,
        *,
        actor=None,
        action: str,
        module: str,
        target_model: str = '',
        target_id: Any = None,
        description: str = '',
        previous_data: Optional[Dict[str, Any]] = None,
        new_data: Optional[Dict[str, Any]] = None,
        resultado: str = 'exitoso',
        request=None,
    ) -> AuditLog:
        ip_address, user_agent, resolved_actor = cls._extract_meta(request=request, actor=actor)
        if resolved_actor:
            cls.set_db_actor_session(resolved_actor)

        parsed_uuid = None
        if target_id:
            try:
                parsed_uuid = uuid.UUID(str(target_id))
            except ValueError:
                parsed_uuid = None

        payload_new = dict(new_data) if isinstance(new_data, dict) else {}
        if description and 'descripcion' not in payload_new:
            payload_new['descripcion'] = description

        return AuditLog.objects.create(
            usuario=resolved_actor,
            accion=str(action).lower(),
            modulo=str(module).lower(),
            tabla_afectada=target_model,
            id_registro=parsed_uuid,
            datos_anteriores=previous_data,
            datos_nuevos=payload_new or None,
            direccion_ip=ip_address,
            user_agent=user_agent,
            resultado=resultado,
        )

    @classmethod
    def log_access(
        cls,
        *,
        actor=None,
        correo_intentado: str = '',
        tipo_evento: str = 'login',
        resultado: str = 'exitoso',
        request=None,
    ) -> AuditAccess:
        ip_address, user_agent, resolved_actor = cls._extract_meta(request=request, actor=actor)
        return AuditAccess.objects.create(
            usuario=resolved_actor,
            correo_intentado=correo_intentado or (getattr(resolved_actor, 'correo', '') if resolved_actor else ''),
            tipo_evento=tipo_evento,
            resultado=resultado,
            direccion_ip=ip_address,
            user_agent=user_agent,
        )

    @classmethod
    def log_case_event(
        cls,
        *,
        caso,
        actor=None,
        tipo_accion: str,
        estado_anterior: str = '',
        estado_nuevo: str = '',
        motivo: str = '',
        request=None,
    ) -> AuditCase:
        _, _, resolved_actor = cls._extract_meta(request=request, actor=actor)
        if resolved_actor:
            cls.set_db_actor_session(resolved_actor)
        return AuditCase.objects.create(
            caso=caso,
            usuario=resolved_actor,
            tipo_accion=tipo_accion,
            estado_anterior=estado_anterior or None,
            estado_nuevo=estado_nuevo or None,
            motivo=motivo or None,
        )

    @classmethod
    def log_permission_change(
        cls,
        *,
        usuario_afectado,
        usuario_responsable=None,
        tipo_cambio: str = 'cambio_rol',
        valor_anterior: Optional[dict] = None,
        valor_nuevo: Optional[dict] = None,
        motivo: str = '',
        request=None,
    ) -> AuditPermission:
        _, _, resolved_actor = cls._extract_meta(request=request, actor=usuario_responsable)
        if resolved_actor:
            cls.set_db_actor_session(resolved_actor)
        return AuditPermission.objects.create(
            usuario_afectado=usuario_afectado,
            usuario_responsable=resolved_actor,
            tipo_cambio=tipo_cambio,
            valor_anterior=valor_anterior,
            valor_nuevo=valor_nuevo,
            motivo=motivo or None,
        )

    @classmethod
    def log_security_event(
        cls,
        *,
        actor=None,
        tipo_evento: str,
        nivel_severidad: str = 'medio',
        descripcion: str = '',
        request=None,
    ) -> AuditSecurity:
        ip_address, _, resolved_actor = cls._extract_meta(request=request, actor=actor)
        return AuditSecurity.objects.create(
            usuario=resolved_actor,
            tipo_evento=tipo_evento,
            nivel_severidad=nivel_severidad,
            descripcion=descripcion,
            direccion_ip=ip_address,
        )
