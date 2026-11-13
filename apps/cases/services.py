from typing import Optional
import uuid as uuid_lib
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import connection, transaction
from django.db.models import Q
from django.utils import timezone

from apps.accounts.models import Role, User
from apps.audit.services import AuditService
from apps.cases.models import (
    Case,
    CaseAssignment,
    CaseContribution,
    CaseCorrectionRequest,
    CaseEvidence,
    CaseStatus,
)
from apps.communications.models import LegalAcceptance
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

AUDIENCE_ALIASES = {
    'PUBLIC': CaseUpdate.Audiencia.PUBLICO,
    'PUBLICO': CaseUpdate.Audiencia.PUBLICO,
    'CITIZEN': CaseUpdate.Audiencia.CIUDADANO,
    'CIUDADANO': CaseUpdate.Audiencia.CIUDADANO,
    'INTERNAL': CaseUpdate.Audiencia.INTERNO,
    'INTERNO': CaseUpdate.Audiencia.INTERNO,
    'PRIVATE': CaseUpdate.Audiencia.INTERNO,
}


class CaseService:
    """
    Servicio de dominio transaccional sobre las tablas de `plus`:
    casos, estados_caso, asignaciones_casos, seguimientos, historial_estados,
    solicitudes_correccion, aportes_caso, evidencias y auditoria_casos.
    """

    @staticmethod
    def user_can_manage_case(user: User, case: Case) -> bool:
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.has_any_role(Role.Nombre.ADMINISTRADOR):
            return True
        if user.has_any_role(Role.Nombre.REPRESENTANTE):
            return case.asignaciones.filter(responsable=user, activo=True).exists()
        return False

    @classmethod
    def get_allowed_actions(cls, user: Optional[User], case: Case) -> list[str]:
        if not user or not user.is_authenticated:
            return ['view_public'] if case.estado_publicacion == Case.EstadoPublicacion.APROBADO else []
        actions = ['view']
        if case.usuario_id == user.id:
            actions.extend(['contribute', 'upload_evidence', 'message'])
        if user.is_superuser or user.has_any_role(Role.Nombre.ADMINISTRADOR):
            actions.extend(['moderate', 'request_correction', 'assign', 'progress', 'resolve', 'manage_evidence', 'message'])
        elif user.has_any_role(Role.Nombre.MODERADOR):
            actions.extend(['moderate', 'request_correction', 'manage_evidence', 'message'])
        elif cls.user_can_manage_case(user, case):
            actions.extend(['progress', 'resolve', 'upload_evidence', 'message'])
        return list(dict.fromkeys(actions))

    @classmethod
    @transaction.atomic
    def register_case(cls, *, reporter: User, validated_data: dict, request=None) -> Case:
        AuditService.set_db_actor_session(reporter)
        estado_inicial = validated_data.pop('estado', None) or CaseStatus.get_default_status()
        validated_data.pop('acepta_tratamiento_datos', None)
        validated_data.pop('accepts_data_policy', None)

        lat = validated_data.pop('latitud', None)
        if lat is None:
            lat = validated_data.pop('exact_latitude', None)
        lon = validated_data.pop('longitud', None)
        if lon is None:
            lon = validated_data.pop('exact_longitude', None)
        ubicacion = validated_data.pop('ubicacion', None)
        if ubicacion is None and lat is not None and lon is not None:
            ubicacion = make_geojson_point(lon, lat)

        case = Case.objects.create(
            usuario=reporter,
            estado=estado_inicial,
            ubicacion=ubicacion,
            **validated_data,
        )

        # P06: Procesar anexos iniciales si se envían en la petición multipart/form-data
        if request and getattr(request, 'FILES', None):
            from django.core.files.storage import default_storage
            import os
            tipo_map = {
                '.jpg': CaseEvidence.TipoArchivo.IMAGEN,
                '.jpeg': CaseEvidence.TipoArchivo.IMAGEN,
                '.png': CaseEvidence.TipoArchivo.IMAGEN,
                '.webp': CaseEvidence.TipoArchivo.IMAGEN,
                '.mp4': CaseEvidence.TipoArchivo.VIDEO,
                '.mp3': CaseEvidence.TipoArchivo.AUDIO,
                '.pdf': CaseEvidence.TipoArchivo.DOCUMENTO,
            }
            files = request.FILES.getlist('files') or request.FILES.getlist('archivos')
            if not files:
                single = request.FILES.get('file') or request.FILES.get('archivo')
                if single:
                    files = [single]
            for f in files:
                ext = os.path.splitext(f.name)[1].lower()
                saved_path = default_storage.save(f'cases/{case.codigo}/evidence/{f.name}', f)
                CaseEvidence.objects.create(
                    caso=case,
                    usuario=reporter,
                    tipo_archivo=tipo_map.get(ext, CaseEvidence.TipoArchivo.DOCUMENTO),
                    ruta_archivo=default_storage.url(saved_path),
                    descripcion=f'Evidencia inicial al radicar caso ({f.name})',
                    audiencia=CaseEvidence.Audiencia.CIUDADANO,
                    estado_revision=CaseEvidence.EstadoRevision.PENDIENTE,
                    nombre_original=f.name[:255],
                    mime_type=getattr(f, 'content_type', None),
                    tamano_bytes=getattr(f, 'size', None),
                )

        # Registrar aceptación legal de radicación (AMP-09)
        LegalAcceptance.record(
            finalidad='radicacion_caso',
            tipo_documento='radicacion_caso',
            usuario=reporter,
            caso=case,
            correo_declarado=reporter.correo,
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
        solicitar_correccion: bool = False,
        request=None,
    ) -> Case:
        if not actor.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR):
            raise PermissionDenied('Solo un Administrador o Moderador puede moderar publicaciones de casos.')

        AuditService.set_db_actor_session(actor)

        # AMP-06: Flujo explícito de solicitud de corrección sin inventar un cuarto estado_publicacion
        if solicitar_correccion or str(estado_publicacion).lower() in ('solicitar_correccion', 'correccion_solicitada', 'correction_requested'):
            if not motivo.strip():
                raise ValidationError({'motivo': 'Debe especificar el motivo o requerimiento de corrección.'})
            CaseCorrectionRequest.objects.create(
                caso=case,
                solicitante=actor,
                motivo=motivo.strip(),
                estado=CaseCorrectionRequest.Estado.ABIERTA,
            )
            if prioridad:
                case.prioridad = PRIORITY_ALIASES.get(prioridad.upper(), prioridad.lower())
                case.save(update_fields=['prioridad', 'fecha_actualizacion'])
            NotificationService.notify(
                recipient=case.usuario,
                notification_type='solicitud_correccion',
                title=f'Solicitud de corrección en tu caso {case.codigo}',
                message=motivo[:200],
                related_case=case,
            )
            return case

        resolved_pub = MODERATION_ALIASES.get(estado_publicacion.upper(), estado_publicacion.lower())
        if resolved_pub == Case.EstadoPublicacion.RECHAZADO and not motivo.strip():
            raise ValidationError({'motivo': 'Debe especificar un motivo justificado para rechazar la publicación.'})

        prev_pub = case.estado_publicacion
        prev_prio = case.prioridad

        case.estado_publicacion = resolved_pub
        if resolved_pub == Case.EstadoPublicacion.APROBADO:
            case.fecha_aprobacion = timezone.now()
            # Cerrar solicitudes de corrección abiertas si el caso fue aprobado
            case.solicitudes_correccion.filter(
                estado__in=[CaseCorrectionRequest.Estado.ABIERTA, CaseCorrectionRequest.Estado.RESPONDIDA]
            ).update(
                estado=CaseCorrectionRequest.Estado.CERRADA,
                revisor=actor,
                fecha_revision=timezone.now(),
            )
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
        motivo: str = '',
        request=None,
    ) -> CaseAssignment:
        if not actor.has_any_role(Role.Nombre.ADMINISTRADOR, Role.Nombre.MODERADOR):
            raise PermissionDenied('Solo un Administrador puede asignar responsables a los casos.')

        if not responsable.has_any_role(Role.Nombre.REPRESENTANTE, Role.Nombre.ADMINISTRADOR) or not responsable.is_active:
            raise ValidationError(
                {'responsable': 'El usuario seleccionado no posee un rol activo de Representante/Responsable o Administrador.'}
            )

        # P10: Validar compatibilidad de ámbitos territoriales o temáticos si es representante
        if not responsable.has_any_role(Role.Nombre.ADMINISTRADOR):
            active_scopes = responsable.asignaciones_ambito.filter(activo=True)
            if active_scopes.exists():
                matches_scope = active_scopes.filter(
                    Q(comunidad_id=case.comunidad_id) | Q(tipo_caso_id=case.tipo_caso_id)
                ).exists()
                if not matches_scope:
                    raise ValidationError(
                        {'responsable': 'El representante seleccionado no tiene ámbito asignado para la comunidad o tipo de caso de este expediente.'}
                    )

        AuditService.set_db_actor_session(actor)
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
                motivo=motivo or f'Asignado a representante: {responsable.full_name}',
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
    def _resolve_status_object(cls, status_identifier) -> CaseStatus:
        if isinstance(status_identifier, CaseStatus):
            return status_identifier
        text = str(status_identifier).strip()
        try:
            uuid_val = uuid_lib.UUID(text)
            obj = CaseStatus.objects.filter(pk=uuid_val).first()
            if obj:
                return obj
        except (ValueError, TypeError):
            pass
        return CaseStatus.get_by_name(text)

    @classmethod
    @transaction.atomic
    def change_management_status(
        cls,
        *,
        case: Case,
        actor: User,
        new_status_name: str,
        motivo: str = '',
        resultado_resumen: Optional[str] = None,
        request=None,
    ) -> Case:
        if not cls.user_can_manage_case(actor, case):
            raise PermissionDenied('No tienes autorización para cambiar el estado operativo de este caso.')

        target_status = cls._resolve_status_object(new_status_name)
        effective_reason = (motivo or resultado_resumen or '').strip()
        if target_status.nombre in (CaseStatus.Nombre.RESUELTO, CaseStatus.Nombre.CERRADO) and not effective_reason:
            raise ValidationError(
                {'motivo': 'Debe especificar el motivo o resultado final al resolver o cerrar un caso.'}
            )

        prev_status = case.estado
        AuditService.set_db_actor_session(actor)

        update_fields = ['estado', 'fecha_actualizacion']
        case.estado = target_status

        # AMP-11: Si es resolución o cierre, persistir resultado narrativo estructurado y seguimiento de resolución
        if target_status.nombre in (CaseStatus.Nombre.RESUELTO, CaseStatus.Nombre.CERRADO):
            res_text = (resultado_resumen or effective_reason).strip()
            tipo_ev = (
                CaseUpdate.TipoEvento.RESOLUCION
                if target_status.nombre == CaseStatus.Nombre.RESUELTO
                else CaseUpdate.TipoEvento.CIERRE
            )
            seg_resolucion = CaseUpdate.objects.create(
                caso=case,
                usuario=actor,
                titulo=f'Resolución del caso ({target_status.nombre})',
                descripcion=res_text,
                audiencia=CaseUpdate.Audiencia.CIUDADANO,
                tipo_evento=tipo_ev,
                visible_publicamente=False,
            )
            case.resultado_resumen = res_text
            case.seguimiento_resolucion = seg_resolucion
            case.usuario_resolucion = actor
            case.fecha_resolucion = timezone.now()
            update_fields.extend([
                'resultado_resumen',
                'seguimiento_resolucion',
                'usuario_resolucion',
                'fecha_resolucion',
            ])

        case.save(update_fields=update_fields)

        if prev_status.id != target_status.id:
            if connection.vendor != 'postgresql':
                CaseStatusHistory.objects.create(
                    caso=case,
                    estado_anterior=prev_status,
                    estado_nuevo=target_status,
                    usuario=actor,
                    motivo=effective_reason or 'Cambio de estado',
                )

            AuditService.log_case_event(
                caso=case,
                actor=actor,
                tipo_accion='estado_operativo',
                estado_anterior=prev_status.nombre,
                estado_nuevo=target_status.nombre,
                motivo=effective_reason or 'Cambio de estado operativo',
                request=request,
            )

            NotificationService.notify(
                recipient=case.usuario,
                notification_type='estado_caso',
                title=f'Actualización de estado: {case.codigo}',
                message=f'Tu caso "{case.titulo}" pasó al estado: {target_status.nombre}. {effective_reason}'.strip(),
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
        titulo: Optional[str] = None,
        audiencia: Optional[str] = None,
        tipo_evento: str = CaseUpdate.TipoEvento.SEGUIMIENTO,
        visible_publicamente: bool = False,
        new_status: Optional[str] = None,
        files=None,
        evidence_ids=None,
        evidence_description: Optional[str] = None,
        evidence_audiencia: Optional[str] = None,
        request=None,
    ) -> CaseUpdate:
        is_reporter = case.usuario_id == author.id
        can_manage = cls.user_can_manage_case(author, case)
        if not (is_reporter or can_manage):
            raise PermissionDenied('No tienes permiso para registrar seguimientos en este caso.')

        if audiencia:
            resolved_audiencia = AUDIENCE_ALIASES.get(str(audiencia).upper(), str(audiencia).lower())
        elif visible_publicamente:
            resolved_audiencia = CaseUpdate.Audiencia.PUBLICO
        else:
            resolved_audiencia = CaseUpdate.Audiencia.INTERNO

        if is_reporter and not can_manage:
            resolved_audiencia = CaseUpdate.Audiencia.CIUDADANO

        AuditService.set_db_actor_session(author)
        seguimiento = CaseUpdate.objects.create(
            caso=case,
            usuario=author,
            titulo=titulo,
            descripcion=descripcion,
            audiencia=resolved_audiencia,
            tipo_evento=tipo_evento,
            visible_publicamente=(resolved_audiencia == CaseUpdate.Audiencia.PUBLICO),
        )

        # P24: Vincular evidencias existentes proporcionadas por UUID
        if evidence_ids:
            str_ids = [str(eid) for eid in evidence_ids]
            matched = case.evidencias.filter(id__in=str_ids)
            found_ids = set(str(e.id) for e in matched)
            missing_ids = [eid for eid in str_ids if eid not in found_ids]
            if missing_ids:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({'evidence_ids': f'Las evidencias {missing_ids} no existen o no pertenecen a este caso.'})
            matched.update(seguimiento=seguimiento)

        # P24: Almacenar y vincular archivos binarios subidos directamente en el avance
        if files:
            import os
            import uuid as uuid_lib
            from django.core.files.storage import default_storage
            from core.validators import validate_file_safety
            from apps.cases.models import CaseEvidence

            tipo_map = {
                '.jpg': CaseEvidence.TipoArchivo.IMAGEN,
                '.jpeg': CaseEvidence.TipoArchivo.IMAGEN,
                '.png': CaseEvidence.TipoArchivo.IMAGEN,
                '.webp': CaseEvidence.TipoArchivo.IMAGEN,
                '.mp4': CaseEvidence.TipoArchivo.VIDEO,
                '.mov': CaseEvidence.TipoArchivo.VIDEO,
                '.webm': CaseEvidence.TipoArchivo.VIDEO,
                '.mp3': CaseEvidence.TipoArchivo.AUDIO,
                '.wav': CaseEvidence.TipoArchivo.AUDIO,
                '.ogg': CaseEvidence.TipoArchivo.AUDIO,
                '.pdf': CaseEvidence.TipoArchivo.DOCUMENTO,
                '.doc': CaseEvidence.TipoArchivo.DOCUMENTO,
                '.docx': CaseEvidence.TipoArchivo.DOCUMENTO,
                '.xls': CaseEvidence.TipoArchivo.DOCUMENTO,
                '.xlsx': CaseEvidence.TipoArchivo.DOCUMENTO,
            }

            if evidence_audiencia:
                ev_aud = AUDIENCE_ALIASES.get(str(evidence_audiencia).upper(), str(evidence_audiencia).lower())
                if ev_aud not in CaseEvidence.Audiencia.values:
                    ev_aud = CaseEvidence.Audiencia.CIUDADANO
            elif resolved_audiencia == CaseUpdate.Audiencia.INTERNO:
                ev_aud = CaseEvidence.Audiencia.PRIVADO
            else:
                # Regla de seguridad P24: no hacer pública una evidencia por el solo hecho
                # de que el seguimiento sea público, salvo especificación explícita.
                ev_aud = CaseEvidence.Audiencia.CIUDADANO

            for f in files:
                validate_file_safety(f)
                ext = os.path.splitext(f.name)[1].lower()
                t_archivo = tipo_map.get(ext, CaseEvidence.TipoArchivo.DOCUMENTO)
                clean_name = os.path.basename(f.name)[:255]
                storage_path = f"cases/{case.codigo}/updates/{uuid_lib.uuid4().hex}_{clean_name}"
                saved_path = default_storage.save(storage_path, f)

                ev_desc = evidence_description or f"Adjunto a seguimiento: {titulo or descripcion[:60]}"
                CaseEvidence.objects.create(
                    caso=case,
                    usuario=author,
                    seguimiento=seguimiento,
                    tipo_archivo=t_archivo,
                    ruta_archivo=saved_path,
                    descripcion=ev_desc,
                    audiencia=ev_aud,
                    estado_revision=CaseEvidence.EstadoRevision.PENDIENTE,
                    nombre_original=clean_name,
                    mime_type=getattr(f, 'content_type', None) or 'application/octet-stream',
                    tamano_bytes=getattr(f, 'size', None),
                )

        if new_status and can_manage:
            cls.change_management_status(
                case=case,
                actor=author,
                new_status_name=new_status,
                motivo=descripcion,
                request=request,
            )

        if can_manage and resolved_audiencia in (CaseUpdate.Audiencia.PUBLICO, CaseUpdate.Audiencia.CIUDADANO):
            NotificationService.notify(
                recipient=case.usuario,
                notification_type='seguimiento_caso',
                title=f'Nuevo avance en tu caso {case.codigo}',
                message=descripcion[:150],
                related_case=case,
            )
        return seguimiento

    @classmethod
    @transaction.atomic
    def add_citizen_contribution(
        cls,
        *,
        case: Case,
        author: User,
        contenido: str,
        solicitud_correccion_id=None,
        files=None,
        request=None,
    ) -> CaseContribution:
        """CIT-08 (AMP-07): Registra un aporte privado del ciudadano y vincula sus archivos adjuntos."""
        if case.usuario_id != author.id and not cls.user_can_manage_case(author, case):
            raise PermissionDenied('Solo el propietario del caso puede registrar aportes ciudadanos.')

        AuditService.set_db_actor_session(author)
        solicitud = None
        if solicitud_correccion_id:
            solicitud = CaseCorrectionRequest.objects.filter(pk=solicitud_correccion_id, caso=case).first()
        if not solicitud:
            solicitud = case.active_correction_request

        contribution = CaseContribution.objects.create(
            caso=case,
            usuario=author,
            solicitud_correccion=solicitud,
            contenido=contenido,
        )

        if solicitud and solicitud.estado == CaseCorrectionRequest.Estado.ABIERTA:
            solicitud.estado = CaseCorrectionRequest.Estado.RESPONDIDA
            solicitud.respuesta = contenido
            solicitud.fecha_respuesta = timezone.now()
            solicitud.save(update_fields=['estado', 'respuesta', 'fecha_respuesta'])

        if files:
            from django.core.files.storage import default_storage
            from core.validators import validate_file_safety
            import os

            for f in files:
                validate_file_safety(f)
                ext = os.path.splitext(f.name)[1].lower()
                tipo_map = {
                    '.jpg': CaseEvidence.TipoArchivo.IMAGEN,
                    '.jpeg': CaseEvidence.TipoArchivo.IMAGEN,
                    '.png': CaseEvidence.TipoArchivo.IMAGEN,
                    '.webp': CaseEvidence.TipoArchivo.IMAGEN,
                    '.mp4': CaseEvidence.TipoArchivo.VIDEO,
                    '.mp3': CaseEvidence.TipoArchivo.AUDIO,
                    '.pdf': CaseEvidence.TipoArchivo.DOCUMENTO,
                }
                saved_path = default_storage.save(f'cases/{case.codigo}/contributions/{f.name}', f)
                CaseEvidence.objects.create(
                    caso=case,
                    usuario=author,
                    aporte=contribution,
                    tipo_archivo=tipo_map.get(ext, CaseEvidence.TipoArchivo.DOCUMENTO),
                    ruta_archivo=default_storage.url(saved_path),
                    descripcion=f'Adjunto en aporte ciudadano ({f.name})',
                    audiencia=CaseEvidence.Audiencia.CIUDADANO,
                    estado_revision=CaseEvidence.EstadoRevision.PENDIENTE,
                    nombre_original=f.name[:255],
                    mime_type=getattr(f, 'content_type', None),
                    tamano_bytes=getattr(f, 'size', None),
                )

        active_assign = case.active_assignment
        if active_assign:
            NotificationService.notify(
                recipient=active_assign.responsable,
                notification_type='aporte_ciudadano',
                title=f'Nuevo aporte ciudadano en {case.codigo}',
                message=contenido[:140],
                related_case=case,
            )
        return contribution
