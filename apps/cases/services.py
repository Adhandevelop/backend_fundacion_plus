from typing import Optional
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import connection, transaction
from django.utils import timezone

from apps.accounts.models import Role, User
from apps.audit.services import AuditService
from apps.cases.models import Case, CaseAssignment, CaseStatus
from apps.notifications.services import NotificationService
from apps.tracking.models import CaseStatusHistory, CaseUpdate
from core.gis import make_geojson_point

MODERATION_ALIASES = {
    'PENDING': Case.EstadoPublicacion.PENDIENTE,
    'PENDIENTE': Case.EstadoPublicacion.PENDIENTE,
    'APPROVED': Case.EstadoPublicacion.APROBADO,
    'APROBADO': Case.EstadoPublicacion.APROBADO,
    'REJECTED': Case.EstadoPublicacion.RECHAZADO,
    'RECHAZADO': Case.EstadoPublicacion.RECHAZADO,
}

PRIORITY_ALIASES = {
    'LOW': Case.Prioridad.BAJA,
    'BAJA': Case.Prioridad.BAJA,
    'MEDIUM': Case.Prioridad.MEDIA,
    'MEDIA': Case.Prioridad.MEDIA,
    'HIGH': Case.Prioridad.ALTA,
    'ALTA': Case.Prioridad.ALTA,
    'CRITICAL': Case.Prioridad.CRITICA,
    'CRITICA': Case.Prioridad.CRITICA,
}


class CaseService:
    """
    Servicio de dominio transaccional sobre las tablas de `plus`:
    casos, estados_caso, asignaciones_casos, seguimientos, historial_estados y auditoria_casos.
    """

    @staticmethod
    def user_can_manage_case(user: User, case: Case) -> bool:
        if not user or not user.is_authenticated:
            return False
        if user.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR):
            return True
        if user.has_any_role(Role.Nombre.REPRESENTANTE):
            return case.asignaciones.filter(responsable=user, activo=True).exists()
        return False

    @classmethod
    @transaction.atomic
    def register_case(cls, *, reporter: User, validated_data: dict, request=None) -> Case:
        AuditService.set_db_actor_session(reporter)
        estado_inicial = validated_data.pop('estado', None) or CaseStatus.get_default_status()

        lat = validated_data.pop('latitud', None) or validated_data.pop('exact_latitude', None)
        lon = validated_data.pop('longitud', None) or validated_data.pop('exact_longitude', None)
        ubicacion = validated_data.pop('ubicacion', None)
        if ubicacion is None and lat is not None and lon is not None:
            ubicacion = make_geojson_point(lon, lat)

        case = Case.objects.create(
            usuario=reporter,
            estado=estado_inicial,
            ubicacion=ubicacion,
            **validated_data,
        )

        # En SQLite creamos el historial desde ORM; en PostgreSQL lo crea el trigger tg_casos_historial
        if connection.vendor != 'postgresql':
            CaseStatusHistory.objects.create(
                caso=case,
                estado_anterior=None,
                estado_nuevo=estado_inicial,
                usuario=reporter,
                motivo='Creacion del caso',
            )

        AuditService.log(
            actor=reporter,
            action='insert',
            module='casos',
            target_model='casos',
            target_id=case.pk,
            description=f'Radicación de nuevo caso {case.codigo}',
            request=request,
        )
        return case

    @classmethod
    @transaction.atomic
    def moderate_case(
        cls,
        *,
        case: Case,
        actor: User,
        estado_publicacion: str,
        motivo: str = '',
        prioridad: Optional[str] = None,
        request=None,
    ) -> Case:
        if not actor.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR):
            raise PermissionDenied('Solo un Administrador o Moderador puede aprobar o rechazar publicaciones.')

        resolved_pub = MODERATION_ALIASES.get(estado_publicacion.upper(), estado_publicacion.lower())
        if resolved_pub == Case.EstadoPublicacion.RECHAZADO and not motivo.strip():
            raise ValidationError({'motivo': 'Debe especificar un motivo justificado para rechazar la publicación.'})

        prev_pub = case.estado_publicacion
        prev_prio = case.prioridad

        AuditService.set_db_actor_session(actor)
        case.estado_publicacion = resolved_pub
        if resolved_pub == Case.EstadoPublicacion.APROBADO:
            case.fecha_aprobacion = timezone.now()
        if prioridad:
            case.prioridad = PRIORITY_ALIASES.get(prioridad.upper(), prioridad.lower())
        case.save()

        if connection.vendor != 'postgresql':
            if prev_pub != case.estado_publicacion:
                AuditService.log_case_event(
                    caso=case,
                    actor=actor,
                    tipo_accion='publicacion',
                    estado_anterior=prev_pub,
                    estado_nuevo=case.estado_publicacion,
                    motivo=motivo or 'Cambio de estado de publicacion',
                    request=request,
                )
            if prev_prio != case.prioridad:
                AuditService.log_case_event(
                    caso=case,
                    actor=actor,
                    tipo_accion='prioridad',
                    estado_anterior=prev_prio,
                    estado_nuevo=case.prioridad,
                    motivo=motivo or 'Cambio de prioridad',
                    request=request,
                )

        NotificationService.notify(
            recipient=case.usuario,
            notification_type='moderacion_caso',
            title=f'Revisión del caso {case.codigo}',
            message=f'El estado de publicación de tu caso "{case.titulo}" cambió a {case.estado_publicacion}. {motivo}'.strip(),
            related_case=case,
        )
        return case

    @classmethod
    @transaction.atomic
    def assign_responsible(
        cls,
        *,
        case: Case,
        actor: User,
        responsable: User,
        request=None,
    ) -> CaseAssignment:
        if not actor.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR):
            raise PermissionDenied('Solo un Administrador puede asignar responsables a los casos.')

        if not responsable.has_any_role(Role.Nombre.REPRESENTANTE, Role.Nombre.ADMINISTRADOR):
            raise ValidationError(
                {'responsable': 'El usuario seleccionado no posee el rol de Representante/Responsable o Administrador.'}
            )

        AuditService.set_db_actor_session(actor)
        # Cerrar asignación activa previa (política ux_asignacion_caso_activa: un responsable activo por caso)
        case.asignaciones.filter(activo=True).update(
            activo=False,
            fecha_finalizacion=timezone.now(),
        )

        assignment = CaseAssignment.objects.create(
            caso=case,
            responsable=responsable,
            asignador=actor,
            activo=True,
        )

        if case.estado.nombre == CaseStatus.Nombre.PENDIENTE:
            cls.change_management_status(
                case=case,
                actor=actor,
                new_status_name=CaseStatus.Nombre.EN_REVISION,
                motivo=f'Asignado a representante: {responsable.full_name}',
                request=request,
            )

        NotificationService.notify(
            recipient=responsable,
            notification_type='asignacion_caso',
            title=f'Nuevo caso asignado: {case.codigo}',
            message=f'Se te ha asignado la gestión del caso "{case.titulo}".',
            related_case=case,
        )
        return assignment

    @classmethod
    @transaction.atomic
    def change_management_status(
        cls,
        *,
        case: Case,
        actor: User,
        new_status_name: str,
        motivo: str = '',
        request=None,
    ) -> Case:
        if not cls.user_can_manage_case(actor, case):
            raise PermissionDenied('No tienes autorización para cambiar el estado operativo de este caso.')

        target_status = CaseStatus.get_by_name(new_status_name)
        if target_status.nombre in (CaseStatus.Nombre.RESUELTO, CaseStatus.Nombre.CERRADO) and not motivo.strip():
            raise ValidationError(
                {'motivo': 'Debe especificar el motivo o resultado final al resolver o cerrar un caso.'}
            )

        prev_status = case.estado
        if prev_status.id == target_status.id:
            return case

        AuditService.set_db_actor_session(actor)
        case.estado = target_status
        case.save(update_fields=['estado', 'fecha_actualizacion'])

        if connection.vendor != 'postgresql':
            CaseStatusHistory.objects.create(
                caso=case,
                estado_anterior=prev_status,
                estado_nuevo=target_status,
                usuario=actor,
                motivo=motivo or 'Cambio de estado',
            )

        AuditService.log_case_event(
            caso=case,
            actor=actor,
            tipo_accion='estado_operativo',
            estado_anterior=prev_status.nombre,
            estado_nuevo=target_status.nombre,
            motivo=motivo or 'Cambio de estado operativo',
            request=request,
        )

        NotificationService.notify(
            recipient=case.usuario,
            notification_type='estado_caso',
            title=f'Actualización de estado: {case.codigo}',
            message=f'Tu caso "{case.titulo}" pasó al estado: {target_status.nombre}. {motivo}'.strip(),
            related_case=case,
        )
        return case

    @classmethod
    @transaction.atomic
    def add_case_update(
        cls,
        *,
        case: Case,
        author: User,
        descripcion: str,
        visible_publicamente: bool = False,
        request=None,
    ) -> CaseUpdate:
        is_reporter = case.usuario_id == author.id
        can_manage = cls.user_can_manage_case(author, case)
        if not (is_reporter or can_manage):
            raise PermissionDenied('No tienes permiso para registrar seguimientos en este caso.')

        if is_reporter and not can_manage:
            visible_publicamente = False

        AuditService.set_db_actor_session(author)
        seguimiento = CaseUpdate.objects.create(
            caso=case,
            usuario=author,
            descripcion=descripcion,
            visible_publicamente=visible_publicamente,
        )

        if can_manage:
            NotificationService.notify(
                recipient=case.usuario,
                notification_type='seguimiento_caso',
                title=f'Nuevo seguimiento en tu caso {case.codigo}',
                message=descripcion[:150],
                related_case=case,
            )
        return seguimiento
