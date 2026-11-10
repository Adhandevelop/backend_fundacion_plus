import csv
import hashlib
import io
import json
import secrets
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.accounts.models import Role, User, UserProfile
from apps.audit.services import AuditService
from apps.communications.models import LegalAcceptance, LegalDocument
from apps.dynamic_forms.models import (
    Formulario,
    FormularioEnvio,
    FormularioNotificacion,
    FormularioOpcion,
    FormularioPregunta,
    FormularioRespuesta,
    FormularioToken,
    FormularioVersion,
)
from apps.dynamic_forms.validators import (
    validate_pregunta_codigo,
    validate_respuesta_contra_pregunta,
)


class FormularioService:
    """Servicio administrativo para el ciclo de vida y versionado de formularios."""

    @classmethod
    @transaction.atomic
    def save_draft(cls, formulario: Formulario, data: dict, actor=None) -> Formulario:
        # Control de concurrencia optimista
        expected_rev = data.get('revision_esperada')
        if expected_rev is not None and int(expected_rev) != formulario.revision_edicion:
            raise ValidationError(
                'El formulario ha sido modificado por otro administrador (conflicto de concurrencia). '
                'Por favor recargue la página para ver los cambios recientes antes de guardar.'
            )

        if 'titulo' in data and data['titulo']:
            formulario.titulo = str(data['titulo']).strip()
        if 'descripcion' in data:
            formulario.descripcion = str(data['descripcion']).strip()
        if 'requiere_documento' in data:
            formulario.requiere_documento = bool(data['requiere_documento'])
        if 'permite_multiples_envios' in data:
            formulario.permite_multiples_envios = bool(data['permite_multiples_envios'])

        formulario.revision_edicion += 1
        formulario.save()

        # Si se envían preguntas en el borrador
        preguntas_data = data.get('preguntas')
        if preguntas_data is not None:
            cls._sync_draft_questions(formulario, preguntas_data)

        if actor:
            AuditService.set_db_actor_session(actor)
            AuditService.log(
                actor=actor,
                action='update',
                module='formularios_dinamicos',
                target_model='formularios',
                target_id=formulario.id,
                description=f'Actualización de borrador en formulario "{formulario.titulo}" (Rev {formulario.revision_edicion})',
            )

        return formulario

    @classmethod
    def _sync_draft_questions(cls, formulario: Formulario, preguntas_data: list):
        # Limpiar preguntas borrador previas y recrear
        formulario.preguntas_borrador.all().delete()
        codigos_vistos = set()

        for idx, p_data in enumerate(preguntas_data, start=1):
            codigo = validate_pregunta_codigo(p_data.get('codigo'))
            if codigo in codigos_vistos:
                raise ValidationError(f'El código de pregunta "{codigo}" está duplicado en el borrador.')
            codigos_vistos.add(codigo)

            pregunta = FormularioPregunta.objects.create(
                formulario_borrador=formulario,
                codigo=codigo,
                enunciado=str(p_data.get('enunciado', '')).strip(),
                descripcion_ayuda=str(p_data.get('descripcion_ayuda', '')).strip(),
                tipo_campo=p_data.get('tipo_campo'),
                es_obligatorio=bool(p_data.get('es_obligatorio', False)),
                orden=int(p_data.get('orden', idx)),
                configuracion_validacion=p_data.get('configuracion_validacion') or {},
            )

            opciones_data = p_data.get('opciones', [])
            for o_idx, o_data in enumerate(opciones_data, start=1):
                FormularioOpcion.objects.create(
                    pregunta=pregunta,
                    valor=str(o_data.get('valor', '')).strip(),
                    etiqueta=str(o_data.get('etiqueta', '')).strip(),
                    orden=int(o_data.get('orden', o_idx)),
                )

    @classmethod
    @transaction.atomic
    def publish_version(cls, formulario: Formulario, actor=None) -> FormularioVersion:
        # Verificar que tenga preguntas en borrador o versión previa
        preguntas_fuente = list(formulario.preguntas_borrador.all())
        if not preguntas_fuente and formulario.numero_version_publicada == 0:
            raise ValidationError('No se puede publicar un formulario sin preguntas configuradas.')

        # Si no hay borrador nuevo pero se pide publicar versión previa
        if not preguntas_fuente:
            ultima_v = formulario.versiones.filter(es_vigente=True).first()
            if ultima_v:
                preguntas_fuente = list(ultima_v.preguntas.all())

        nueva_version_num = formulario.numero_version_publicada + 1

        # Desmarcar versiones vigentes anteriores
        formulario.versiones.filter(es_vigente=True).update(es_vigente=False)

        # Crear versión congelada inmutable
        version = FormularioVersion.objects.create(
            formulario=formulario,
            numero_version=nueva_version_num,
            es_vigente=True,
            titulo_congelado=formulario.titulo,
            descripcion_congelada=formulario.descripcion,
            requiere_documento=formulario.requiere_documento,
            permite_multiples_envios=formulario.permite_multiples_envios,
            publicado_en=timezone.now(),
            publicado_por=actor,
        )

        # Copiar preguntas y opciones a la versión inmutable
        for pf in preguntas_fuente:
            p_nueva = FormularioPregunta.objects.create(
                version=version,
                codigo=pf.codigo,
                enunciado=pf.enunciado,
                descripcion_ayuda=pf.descripcion_ayuda,
                tipo_campo=pf.tipo_campo,
                es_obligatorio=pf.es_obligatorio,
                orden=pf.orden,
                configuracion_validacion=pf.configuracion_validacion,
            )
            for op in pf.opciones.all():
                FormularioOpcion.objects.create(
                    pregunta=p_nueva,
                    valor=op.valor,
                    etiqueta=op.etiqueta,
                    orden=op.orden,
                )

        formulario.estado = Formulario.Estado.PUBLICADO
        formulario.numero_version_publicada = nueva_version_num
        formulario.save()

        if actor:
            AuditService.set_db_actor_session(actor)
            AuditService.log(
                actor=actor,
                action='publish',
                module='formularios_dinamicos',
                target_model='formulario_versiones',
                target_id=version.id,
                description=f'Publicación de la versión {nueva_version_num} del formulario "{formulario.titulo}"',
            )

        return version

    @classmethod
    def close_formulario(cls, formulario: Formulario, actor=None) -> Formulario:
        formulario.estado = Formulario.Estado.CERRADO
        formulario.save()
        if actor:
            AuditService.set_db_actor_session(actor)
            AuditService.log(
                actor=actor,
                action='update',
                module='formularios_dinamicos',
                target_model='formularios',
                target_id=formulario.id,
                description=f'Cierre de formulario "{formulario.titulo}" para nuevos envíos',
            )
        return formulario

    @classmethod
    def reopen_formulario(cls, formulario: Formulario, actor=None) -> Formulario:
        if formulario.estado == Formulario.Estado.ARCHIVADO:
            raise ValidationError('Un formulario archivado no puede ser reabierto. Debe duplicarlo si desea reactivarlo.')
        formulario.estado = Formulario.Estado.PUBLICADO
        formulario.save()
        if actor:
            AuditService.set_db_actor_session(actor)
            AuditService.log(
                actor=actor,
                action='update',
                module='formularios_dinamicos',
                target_model='formularios',
                target_id=formulario.id,
                description=f'Reapertura de formulario "{formulario.titulo}"',
            )
        return formulario

    @classmethod
    def archive_formulario(cls, formulario: Formulario, actor=None) -> Formulario:
        formulario.estado = Formulario.Estado.ARCHIVADO
        formulario.save()
        if actor:
            AuditService.set_db_actor_session(actor)
            AuditService.log(
                actor=actor,
                action='archive',
                module='formularios_dinamicos',
                target_model='formularios',
                target_id=formulario.id,
                description=f'Archivo histórico de formulario "{formulario.titulo}"',
            )
        return formulario

    @classmethod
    @transaction.atomic
    def duplicate_formulario(cls, formulario: Formulario, actor=None) -> Formulario:
        nuevo_slug = f'{formulario.slug}-copia'
        counter = 1
        while Formulario.objects.filter(slug=nuevo_slug).exists():
            counter += 1
            nuevo_slug = f'{formulario.slug}-copia-{counter}'

        nuevo_form = Formulario.objects.create(
            slug=nuevo_slug,
            titulo=f'{formulario.titulo} (Copia)',
            descripcion=formulario.descripcion,
            estado=Formulario.Estado.BORRADOR,
            requiere_documento=formulario.requiere_documento,
            permite_multiples_envios=formulario.permite_multiples_envios,
            creado_por=actor,
        )

        # Copiar preguntas desde borrador o última versión publicada
        preguntas_origen = list(formulario.preguntas_borrador.all())
        if not preguntas_origen:
            v = formulario.versiones.filter(es_vigente=True).first()
            if v:
                preguntas_origen = list(v.preguntas.all())

        for p in preguntas_origen:
            nueva_p = FormularioPregunta.objects.create(
                formulario_borrador=nuevo_form,
                codigo=p.codigo,
                enunciado=p.enunciado,
                descripcion_ayuda=p.descripcion_ayuda,
                tipo_campo=p.tipo_campo,
                es_obligatorio=p.es_obligatorio,
                orden=p.orden,
                configuracion_validacion=p.configuracion_validacion,
            )
            for op in p.opciones.all():
                FormularioOpcion.objects.create(
                    pregunta=nueva_p,
                    valor=op.valor,
                    etiqueta=op.etiqueta,
                    orden=op.orden,
                )

        if actor:
            AuditService.set_db_actor_session(actor)
            AuditService.log(
                actor=actor,
                action='create',
                module='formularios_dinamicos',
                target_model='formularios',
                target_id=nuevo_form.id,
                description=f'Duplicación del formulario "{formulario.titulo}" a nuevo borrador "{nuevo_form.titulo}"',
            )

        return nuevo_form

    @classmethod
    @transaction.atomic
    def create_draft_from_version(cls, formulario: Formulario, version_num: int, actor=None) -> Formulario:
        version = formulario.versiones.filter(numero_version=version_num).first()
        if not version:
            raise ValidationError(f'No existe la versión {version_num} para este formulario.')

        formulario.preguntas_borrador.all().delete()
        for p in version.preguntas.all():
            nueva_p = FormularioPregunta.objects.create(
                formulario_borrador=formulario,
                codigo=p.codigo,
                enunciado=p.enunciado,
                descripcion_ayuda=p.descripcion_ayuda,
                tipo_campo=p.tipo_campo,
                es_obligatorio=p.es_obligatorio,
                orden=p.orden,
                configuracion_validacion=p.configuracion_validacion,
            )
            for op in p.opciones.all():
                FormularioOpcion.objects.create(
                    pregunta=nueva_p,
                    valor=op.valor,
                    etiqueta=op.etiqueta,
                    orden=op.orden,
                )

        formulario.revision_edicion += 1
        formulario.save()
        return formulario


class FormularioTokenService:
    """Gestión segura de tokens con hash SHA-256 para activación y reivindicación."""

    @classmethod
    def create_token(cls, usuario: User | None, correo: str, proposito: str, ip: str | None = None) -> tuple[str, FormularioToken]:
        # Invalidar tokens previos del mismo correo y propósito
        FormularioToken.objects.filter(
            correo__iexact=correo.strip().lower(),
            proposito=proposito,
            usado=False,
        ).update(usado=True)

        raw_token = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        timeout_seconds = getattr(settings, 'FORM_ACCOUNT_ACTIVATION_TIMEOUT', 172800)
        expira_en = timezone.now() + timedelta(seconds=timeout_seconds)

        token_obj = FormularioToken.objects.create(
            usuario=usuario,
            correo=correo.strip().lower(),
            token_hash=token_hash,
            proposito=proposito,
            fecha_expiracion=expira_en,
            ip_creacion=ip,
        )
        return raw_token, token_obj

    @classmethod
    @transaction.atomic
    def verify_and_activate(cls, raw_token: str, nueva_contrasena: str, ip: str | None = None) -> User:
        clean_token = (raw_token or '').strip()
        token_hash = hashlib.sha256(clean_token.encode()).hexdigest()

        token_obj = FormularioToken.objects.filter(token_hash=token_hash).first()
        if not token_obj:
            raise ValidationError('El enlace de activación es inválido o no existe.')
        if token_obj.usado:
            raise ValidationError('Este enlace ya ha sido utilizado previamente.')
        if token_obj.is_expired:
            raise ValidationError('El enlace de activación ha vencido (plazo de 48 horas superado). Por favor solicite un nuevo enlace.')

        token_obj.usado = True
        token_obj.fecha_uso = timezone.now()
        token_obj.ip_uso = ip
        token_obj.save()

        user = token_obj.usuario
        if not user:
            user = User.objects.filter(correo__iexact=token_obj.correo).first()
        if not user:
            raise ValidationError('No se encontró una cuenta ciudadana asociada a este enlace.')

        # Fijar contraseña y activar cuenta
        user.set_password(nueva_contrasena)
        user.estado = User.Estado.ACTIVO
        user.save()

        # Vincular automáticamente todos los envíos pendientes del correo
        FormularioEnvio.objects.filter(
            correo_declarado__iexact=user.correo,
            estado_vinculacion__in=[
                FormularioEnvio.EstadoVinculacion.PENDIENTE_ACTIVACION,
                FormularioEnvio.EstadoVinculacion.PENDIENTE_REIVINDICACION,
            ],
        ).update(
            usuario=user,
            estado_vinculacion=FormularioEnvio.EstadoVinculacion.VINCULADO,
        )

        AuditService.set_db_actor_session(user)
        AuditService.log(
            actor=user,
            action='update',
            module='cuentas',
            target_model='usuarios',
            target_id=user.id,
            description=f'Activación exitosa de cuenta ciudadana mediante formulario ({user.correo})',
        )

        return user

    @classmethod
    def resend_token(cls, correo: str, ip: str | None = None) -> bool:
        norm_email = (correo or '').strip().lower()
        if not norm_email or '@' not in norm_email:
            return False

        # Rate limit: máx 3 solicitudes en 15 min por correo
        hace_15m = timezone.now() - timedelta(minutes=15)
        count_email = FormularioToken.objects.filter(correo=norm_email, fecha_creacion__gte=hace_15m).count()
        if count_email >= 3:
            return True  # Respuesta neutral sin error para evitar enumeración

        user = User.objects.filter(correo__iexact=norm_email).first()
        envio_pendiente = FormularioEnvio.objects.filter(
            correo_declarado__iexact=norm_email,
            estado_vinculacion__in=[
                FormularioEnvio.EstadoVinculacion.PENDIENTE_ACTIVACION,
                FormularioEnvio.EstadoVinculacion.PENDIENTE_REIVINDICACION,
            ],
        ).first()

        if not envio_pendiente:
            return True  # Neutral

        proposito = (
            FormularioToken.Proposito.ACTIVAR_CUENTA
            if envio_pendiente.estado_vinculacion == FormularioEnvio.EstadoVinculacion.PENDIENTE_ACTIVACION
            else FormularioToken.Proposito.REIVINDICAR_ENVIO
        )

        raw_token, token_obj = cls.create_token(usuario=user, correo=norm_email, proposito=proposito, ip=ip)
        FormularioNotificationService.enqueue_activation_email(
            envio=envio_pendiente,
            correo=norm_email,
            raw_token=raw_token,
            proposito=proposito,
        )
        return True


class FormularioNotificationService:
    """Despacho desacoplado y resiliente de notificaciones por correo."""

    @classmethod
    def enqueue_activation_email(cls, envio: FormularioEnvio, correo: str, raw_token: str, proposito: str):
        asunto = f'Activación de cuenta en PLUS — Formulario: {envio.formulario.titulo}'
        enlace = f'{getattr(settings, "FRONTEND_URL", "http://localhost:4200")}/activar-cuenta?token={raw_token}'

        cuerpo = (
            f'Hola {envio.nombres_declarados},\n\n'
            f'Hemos recibido tu respuesta al formulario "{envio.formulario.titulo}".\n\n'
            f'Para consultar tus respuestas, gestionar trámites ciudadanos y proteger tu información, '
            f'por favor activa tu cuenta ciudadana y crea tu contraseña ingresando al siguiente enlace:\n\n'
            f'{enlace}\n\n'
            f'Este enlace es de un solo uso y vencerá en 48 horas.\n'
            f'Si no reconoces esta solicitud o no diligenciaste ningún formulario, puedes ignorar este mensaje.\n\n'
            f'Equipo de la Corporación PLUS.'
        )

        notif = FormularioNotificacion.objects.create(
            envio=envio,
            correo_destino=correo,
            asunto=asunto,
            cuerpo_texto=cuerpo,
            estado=FormularioNotificacion.Estado.PENDIENTE,
        )

        try:
            send_mail(
                subject=asunto,
                message=cuerpo,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'contacto@plus.org'),
                recipient_list=[correo],
                fail_silently=False,
            )
            notif.estado = FormularioNotificacion.Estado.ENVIADO
            notif.fecha_envio = timezone.now()
            notif.save()
        except Exception as exc:
            notif.estado = FormularioNotificacion.Estado.FALLIDO
            notif.error_mensaje = str(exc)[:500]
            notif.intentos += 1
            notif.save()


class FormularioSubmissionService:
    """Procesamiento transaccional e idempotente del envío público del formulario."""

    @classmethod
    @transaction.atomic
    def process_submission(cls, formulario: Formulario, validated_data: dict, request, idempotency_key=None) -> FormularioEnvio:
        payload_json = json.dumps(validated_data, sort_keys=True, default=str)
        payload_hash = hashlib.sha256(payload_json.encode()).hexdigest()

        # Idempotencia estricta
        if idempotency_key:
            previo = FormularioEnvio.objects.filter(idempotency_key=idempotency_key).first()
            if previo:
                if previo.idempotency_hash == payload_hash:
                    return previo  # Reentrega idempotente segura
                raise ValidationError('Conflicto: la cabecera Idempotency-Key ya fue utilizada con un contenido diferente.')

        if formulario.estado != Formulario.Estado.PUBLICADO:
            raise ValidationError('El formulario no se encuentra disponible para recibir respuestas.')

        version = formulario.versiones.filter(es_vigente=True).first()
        if not version:
            raise ValidationError('El formulario no cuenta con una versión pública vigente.')

        ident = validated_data['datos_identificacion']
        nombres = ident['nombres'].strip()
        apellidos = ident['apellidos'].strip()
        correo = ident['correo'].strip().lower()
        telefono = ident.get('telefono', '').strip()
        tipo_doc = ident.get('tipo_documento', '').strip()
        num_doc = ident.get('numero_documento', '').strip()

        if version.requiere_documento and (not tipo_doc or not num_doc):
            raise ValidationError('Este formulario exige indicar el tipo y número de documento de identidad.')

        # Validación de duplicados cuando no se permiten múltiples envíos (neutral para visitantes)
        if not version.permite_multiples_envios:
            if request.user.is_authenticated:
                ya_envio = FormularioEnvio.objects.filter(formulario=formulario, usuario=request.user).first()
                if ya_envio:
                    return ya_envio
            else:
                ya_envio = FormularioEnvio.objects.filter(
                    formulario=formulario,
                    correo_declarado__iexact=correo,
                ).first()
                if ya_envio:
                    return ya_envio

        # Validación legal estricta
        id_doc_legal = validated_data['id_documento_legal']
        doc_legal = LegalDocument.get_current('tratamiento_datos')
        if not doc_legal or doc_legal.id != id_doc_legal:
            raise ValidationError('La política de tratamiento de datos informada no está vigente o no coincide con la del formulario.')

        ip_origen = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1')).split(',')[0].strip()
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        user_auth = request.user if request.user.is_authenticated else None
        acceptance = LegalAcceptance.record(
            finalidad='registro_formulario_dinamico',
            tipo_documento='tratamiento_datos',
            usuario=user_auth,
            correo_declarado=correo,
        )

        # Validación rigurosa de cada pregunta contra la versión activa
        preguntas_map = {str(p.id): p for p in version.preguntas.all()}
        respuestas_in = validated_data.get('respuestas', [])
        ids_recibidos = set()
        respuestas_procesadas = []

        for r in respuestas_in:
            p_id_str = str(r['id_pregunta'])
            if p_id_str not in preguntas_map:
                raise ValidationError(f'La pregunta con ID "{p_id_str}" no pertenece a la versión activa del formulario.')
            if p_id_str in ids_recibidos:
                raise ValidationError(f'Pregunta duplicada en el envío: {p_id_str}')
            ids_recibidos.add(p_id_str)

            p_obj = preguntas_map[p_id_str]
            validados = validate_respuesta_contra_pregunta(p_obj, r)
            respuestas_procesadas.append((p_obj, validados))

        # Comprobar que no falten preguntas obligatorias
        for p_id_str, p_obj in preguntas_map.items():
            if p_obj.es_obligatorio and p_id_str not in ids_recibidos:
                raise ValidationError(f'Falta responder la pregunta obligatoria: "{p_obj.enunciado}".')

        # Resolución de identidad y cuentas existentes
        target_user = None
        estado_vinc = FormularioEnvio.EstadoVinculacion.PENDIENTE_ACTIVACION
        proposito_token = None

        if user_auth:
            if user_auth.get_primary_role() == Role.Nombre.CIUDADANO:
                target_user = user_auth
                estado_vinc = FormularioEnvio.EstadoVinculacion.VINCULADO
            else:
                target_user = None
                estado_vinc = FormularioEnvio.EstadoVinculacion.CONTACTO_INSTITUCIONAL
        else:
            existing_user = User.objects.filter(correo__iexact=correo).first()
            if existing_user:
                if existing_user.get_primary_role() != Role.Nombre.CIUDADANO:
                    estado_vinc = FormularioEnvio.EstadoVinculacion.CONTACTO_INSTITUCIONAL
                elif not existing_user.is_active:
                    estado_vinc = FormularioEnvio.EstadoVinculacion.RECHAZADO_POR_POLITICA
                else:
                    target_user = existing_user
                    estado_vinc = FormularioEnvio.EstadoVinculacion.PENDIENTE_REIVINDICACION
                    proposito_token = FormularioToken.Proposito.REIVINDICAR_ENVIO
            else:
                # Comprobar conflicto de cédula: si este documento ya fue declarado previamente con otro correo
                if num_doc and FormularioEnvio.objects.filter(numero_documento_declarado=num_doc).exclude(correo_declarado__iexact=correo).exists():
                    estado_vinc = FormularioEnvio.EstadoVinculacion.PENDIENTE_VERIFICACION
                else:
                    # Crear usuario ciudadano inactivo
                    target_user = User.objects.create_user(
                        email=correo,
                        username=correo.split('@')[0],
                        nombres=nombres,
                        apellidos=apellidos,
                        telefono=telefono,
                        rol=Role.objects.filter(nombre=Role.Nombre.CIUDADANO).first(),
                        is_active=False,
                    )
                    UserProfile.objects.get_or_create(usuario=target_user)

                    estado_vinc = FormularioEnvio.EstadoVinculacion.PENDIENTE_ACTIVACION
                    proposito_token = FormularioToken.Proposito.ACTIVAR_CUENTA

        envio = FormularioEnvio.objects.create(
            formulario=formulario,
            version=version,
            usuario=target_user if estado_vinc == FormularioEnvio.EstadoVinculacion.VINCULADO else None,
            estado_vinculacion=estado_vinc,
            nombres_declarados=nombres,
            apellidos_declarados=apellidos,
            correo_declarado=correo,
            telefono_declarado=telefono,
            tipo_documento_declarado=tipo_doc,
            numero_documento_declarado=num_doc,
            aceptacion_legal=acceptance,
            ip_origen=ip_origen,
            user_agent=user_agent,
            idempotency_key=idempotency_key,
            idempotency_hash=payload_hash,
        )

        for p_obj, vals in respuestas_procesadas:
            FormularioRespuesta.objects.create(
                envio=envio,
                pregunta=p_obj,
                codigo_pregunta=p_obj.codigo,
                enunciado_congelado=p_obj.enunciado,
                tipo_campo_congelado=p_obj.tipo_campo,
                valor_texto=vals['valor_texto'],
                valor_numero=vals['valor_numero'],
                valor_fecha=vals['valor_fecha'],
                valor_booleano=vals['valor_booleano'],
                valores_seleccionados=vals['valores_seleccionados'],
            )

        if proposito_token:
            raw_token, token_obj = FormularioTokenService.create_token(
                usuario=target_user,
                correo=correo,
                proposito=proposito_token,
                ip=ip_origen,
            )
            FormularioNotificationService.enqueue_activation_email(
                envio=envio,
                correo=correo,
                raw_token=raw_token,
                proposito=proposito_token,
            )

        return envio


class FormularioExportService:
    """Generación de CSV seguro con protección contra inyección y BOM UTF-8."""

    @classmethod
    def export_csv(cls, formulario: Formulario, version_num: int | None = None) -> str:
        version = None
        if version_num:
            version = formulario.versiones.filter(numero_version=version_num).first()
        if not version:
            version = formulario.versiones.filter(es_vigente=True).first()

        envios_qs = FormularioEnvio.objects.filter(formulario=formulario)
        if version:
            envios_qs = envios_qs.filter(version=version)

        preguntas = list(version.preguntas.all().order_by('orden')) if version else []

        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

        def sanitize(cell_val):
            val_str = str(cell_val) if cell_val is not None else ''
            if val_str.startswith(('=', '+', '-', '@')):
                return f"'{val_str}"
            return val_str

        headers = [
            'ID_Envio',
            'Numero_Version',
            'Fecha_Envio',
            'Estado_Vinculacion',
            'Nombres',
            'Apellidos',
            'Correo',
            'Telefono',
            'Tipo_Documento',
            'Numero_Documento',
        ]
        for p in preguntas:
            headers.append(f'{p.codigo} ({p.enunciado[:30]})')

        writer.writerow(headers)

        for e in envios_qs.prefetch_related('respuestas'):
            resp_map = {r.codigo_pregunta: r for r in e.respuestas.all()}
            row = [
                sanitize(e.id),
                sanitize(e.version.numero_version),
                sanitize(e.fecha_envio.isoformat()),
                sanitize(e.estado_vinculacion),
                sanitize(e.nombres_declarados),
                sanitize(e.apellidos_declarados),
                sanitize(e.correo_declarado),
                sanitize(e.telefono_declarado),
                sanitize(e.tipo_documento_declarado),
                sanitize(e.numero_documento_declarado),
            ]
            for p in preguntas:
                r = resp_map.get(p.codigo)
                if not r:
                    row.append('')
                else:
                    tipo = r.tipo_campo_congelado
                    if tipo in ('texto_corto', 'texto_largo'):
                        row.append(sanitize(r.valor_texto))
                    elif tipo == 'numero':
                        row.append(sanitize(r.valor_numero))
                    elif tipo == 'fecha':
                        row.append(sanitize(r.valor_fecha))
                    elif tipo == 'booleano':
                        row.append('Sí' if r.valor_booleano else ('No' if r.valor_booleano is False else ''))
                    elif tipo == 'seleccion_unica':
                        row.append(sanitize(r.valor_texto))
                    elif tipo == 'seleccion_multiple':
                        row.append(sanitize(', '.join(r.valores_seleccionados)))
                    else:
                        row.append(sanitize(r.valor_texto))
            writer.writerow(row)

        return '\ufeff' + output.getvalue()
