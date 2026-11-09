from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, permissions, serializers as drf_serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Role, User, UserPreference
from apps.accounts.permissions import IsAdminOrSuperAdmin, IsCitizen
from apps.audit.services import AuditService
from apps.cases.models import Case
from apps.cases.services import CaseService
from apps.cases.views import resolve_case_by_ref
from apps.communications.models import (
    CaseComment,
    CaseMessage,
    EventProposal,
    LegalAcceptance,
    LegalDocument,
    NewsletterSubscription,
    SiteSetting,
)
from apps.communications.serializers import (
    AdminEventProposalSerializer,
    CaseCommentSerializer,
    CaseMessageSerializer,
    CommentModerationActionSerializer,
    EventProposalSerializer,
    LegalDocumentSerializer,
    NewsletterSubscriptionSerializer,
    NewsletterTokenActionSerializer,
    PublicCaseCommentSerializer,
    SiteSettingSerializer,
)
from apps.notifications.services import NotificationService


PUBLIC_SITE_SETTING_KEYS = {
    'institucion.nombre',
    'mapa.srid',
    'iniciativas.max_destacadas',
    'INSTITUTION_HERO',
    'CONTACT_INFO',
    'SOCIAL_LINKS',
}


class MeConversationListView(APIView):
    """
    MSG-01: GET /api/v1/me/conversations/
    Agrupa los mensajes privados permitidos al usuario autenticado por caso y contraparte.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='MeConversationListResponse',
                fields={
                    'count': drf_serializers.IntegerField(),
                    'results': drf_serializers.ListField(
                        child=inline_serializer(
                            name='ConversationSummaryItem',
                            fields={
                                'id_caso': drf_serializers.UUIDField(allow_null=True),
                                'caso_codigo': drf_serializers.CharField(allow_null=True),
                                'caso_titulo': drf_serializers.CharField(allow_null=True),
                                'contraparte_id': drf_serializers.UUIDField(),
                                'contraparte_nombre': drf_serializers.CharField(),
                                'ultimo_mensaje': drf_serializers.CharField(),
                                'fecha_ultimo_mensaje': drf_serializers.DateTimeField(),
                                'unread_count': drf_serializers.IntegerField(),
                            },
                        )
                    ),
                },
            )
        },
        summary='Listar conversaciones privadas agrupadas por caso y contraparte (MSG-01)',
    )
    def get(self, request):
        user = request.user
        msgs = (
            CaseMessage.objects.filter(Q(remitente=user) | Q(destinatario=user))
            .select_related('caso', 'remitente', 'destinatario')
            .order_by('-fecha_envio')
        )
        conversations = {}
        for m in msgs:
            counterpart = m.destinatario if m.remitente_id == user.id else m.remitente
            key = f"{m.caso_id or 'general'}:{counterpart.id}"
            if key not in conversations:
                conversations[key] = {
                    'id_caso': str(m.caso_id) if m.caso_id else None,
                    'caso_codigo': m.caso.codigo if m.caso else None,
                    'caso_titulo': m.caso.titulo if m.caso else 'Conversación general',
                    'counterpart': {
                        'id_usuario': str(counterpart.id),
                        'nombre': counterpart.full_name,
                        'rol': counterpart.get_primary_role(),
                    },
                    'last_message': {
                        'id_mensaje': str(m.id),
                        'contenido': m.contenido,
                        'fecha_envio': m.fecha_envio,
                        'remitente': str(m.remitente_id),
                    },
                    'unread_count': 0,
                }
            if m.destinatario_id == user.id and m.fecha_lectura is None:
                conversations[key]['unread_count'] += 1

        return Response(list(conversations.values()))


class CasePrivateMessageListCreateView(APIView):
    """
    MSG-02 y MSG-03:
    GET / POST /api/v1/cases/{case_id}/messages/, /api/v1/citizen/cases/{case_id}/messages/ y /api/v1/admin/cases/{case_id}/messages/
    Restringe el acceso estrictamente al ciudadano propietario, al responsable asignado o al administrador.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CaseMessageSerializer

    def _get_authorized_case(self, request, case_id) -> Case:
        case = resolve_case_by_ref(Case.objects.all(), case_id)
        is_reporter = case.usuario_id == request.user.id
        can_manage = CaseService.user_can_manage_case(request.user, case)
        if not (is_reporter or can_manage):
            raise PermissionDenied('No tienes autorización para acceder a los mensajes privados de este caso.')
        return case

    def get(self, request, case_id):
        case = self._get_authorized_case(request, case_id)
        messages_qs = case.mensajes_privados.select_related('remitente', 'destinatario').all()
        if not request.user.has_any_role(Role.Nombre.ADMINISTRADOR):
            messages_qs = messages_qs.filter(
                Q(remitente=request.user) | Q(destinatario=request.user)
            )
        if counterpart_id := request.query_params.get('counterpart'):
            messages_qs = messages_qs.filter(
                Q(remitente_id=counterpart_id) | Q(destinatario_id=counterpart_id)
            )
        messages_qs.filter(destinatario=request.user, fecha_lectura__isnull=True).update(
            fecha_lectura=timezone.now(),
        )
        return Response(CaseMessageSerializer(messages_qs, many=True).data)

    def post(self, request, case_id):
        case = self._get_authorized_case(request, case_id)
        serializer = CaseMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        destinatario = serializer.validated_data.get('destinatario')
        if not destinatario:
            if request.user.id == case.usuario_id:
                active_assign = case.active_assignment
                if active_assign and active_assign.responsable_id != request.user.id:
                    destinatario = active_assign.responsable
                else:
                    destinatario = (
                        User.objects.filter(
                            rol__nombre__in=[Role.Nombre.ADMINISTRADOR, Role.Nombre.REPRESENTANTE],
                            estado=User.Estado.ACTIVO,
                        )
                        .exclude(pk=request.user.id)
                        .first()
                    )
            else:
                destinatario = case.usuario

        if not destinatario or destinatario.id == request.user.id:
            return Response(
                {
                    'code': 'validation_error',
                    'message': 'El remitente y el destinatario del mensaje privado deben ser distintos.',
                    'errors': {'destinatario': ['Destinatario inválido.']},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        msg = serializer.save(caso=case, remitente=request.user, destinatario=destinatario)

        NotificationService.notify(
            recipient=destinatario,
            notification_type='mensaje_privado',
            title=f'Nuevo mensaje privado en {case.codigo}',
            message=msg.contenido[:140],
            related_case=case,
        )
        return Response(CaseMessageSerializer(msg).data, status=status.HTTP_201_CREATED)


class CasePrivateMessageMarkReadView(APIView):
    """
    MSG-04: PUT / POST /api/v1/cases/{case_id}/messages/read/
    Marca como leídos únicamente los mensajes destinados al usuario autenticado,
    soportando selección por lista (`message_ids`), corte por mensaje (`up_to_message_id`)
    o corte temporal (`up_to_timestamp`) para no marcar mensajes recibidos después de abrir la conversación.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=inline_serializer(
            name='MarkMessagesReadRequest',
            fields={
                'message_ids': drf_serializers.ListField(
                    child=drf_serializers.UUIDField(),
                    required=False,
                    help_text='Lista opcional de UUIDs de mensajes recibidos a marcar como leídos.',
                ),
                'up_to_message_id': drf_serializers.UUIDField(
                    required=False,
                    help_text='UUID del último mensaje visible en pantalla; marca como leídos hasta ese mensaje inclusive.',
                ),
                'up_to_timestamp': drf_serializers.DateTimeField(
                    required=False,
                    help_text='Fecha/hora ISO de corte; excluye mensajes recibidos con fecha posterior.',
                ),
            },
        ),
        responses={
            200: inline_serializer(
                name='MarkMessagesReadResponse',
                fields={
                    'marked_read': drf_serializers.IntegerField(),
                    'unread_remaining': drf_serializers.IntegerField(),
                },
            )
        },
        summary='Marcar mensajes privados recibidos como leídos con corte opcional (MSG-04)',
    )
    def post(self, request, case_id):
        return self.put(request, case_id)

    @extend_schema(
        request=inline_serializer(
            name='MarkMessagesReadPutRequest',
            fields={
                'message_ids': drf_serializers.ListField(
                    child=drf_serializers.UUIDField(),
                    required=False,
                    help_text='Lista opcional de UUIDs de mensajes recibidos a marcar como leídos.',
                ),
                'up_to_message_id': drf_serializers.UUIDField(
                    required=False,
                    help_text='UUID del último mensaje visible en pantalla; marca como leídos hasta ese mensaje inclusive.',
                ),
                'up_to_timestamp': drf_serializers.DateTimeField(
                    required=False,
                    help_text='Fecha/hora ISO de corte; excluye mensajes recibidos con fecha posterior.',
                ),
            },
        ),
        responses={
            200: inline_serializer(
                name='MarkMessagesReadPutResponse',
                fields={
                    'marked_read': drf_serializers.IntegerField(),
                    'unread_remaining': drf_serializers.IntegerField(),
                },
            )
        },
        summary='Marcar mensajes privados recibidos como leídos con corte opcional (MSG-04)',
    )
    def put(self, request, case_id):
        from django.utils.dateparse import parse_datetime

        case = resolve_case_by_ref(Case.objects.all(), case_id)
        qs = case.mensajes_privados.filter(destinatario=request.user, fecha_lectura__isnull=True)
        message_ids = request.data.get('message_ids') or request.data.get('ids')
        up_to_msg_id = request.data.get('up_to_message_id') or request.data.get('hasta_id_mensaje')
        up_to_ts = request.data.get('up_to_timestamp') or request.data.get('hasta_fecha')

        if isinstance(message_ids, list) and message_ids:
            qs = qs.filter(id__in=message_ids)
        if up_to_msg_id:
            cutoff_msg = case.mensajes_privados.filter(id=up_to_msg_id).first()
            if cutoff_msg:
                qs = qs.filter(fecha_envio__lte=cutoff_msg.fecha_envio)
        if up_to_ts:
            parsed_dt = parse_datetime(str(up_to_ts))
            if parsed_dt:
                qs = qs.filter(fecha_envio__lte=parsed_dt)

        updated = qs.update(fecha_lectura=timezone.now())
        remaining = case.mensajes_privados.filter(destinatario=request.user, fecha_lectura__isnull=True).count()
        return Response({'marked_read': updated, 'unread_remaining': remaining}, status=status.HTTP_200_OK)


class PublicCaseCommentListView(generics.ListAPIView):
    """
    MAP-06: GET /api/v1/public/cases/{case_id}/comments/
    Retorna comentarios con `estado_moderacion='aprobado'` sobre un caso aprobado.
    """
    serializer_class = PublicCaseCommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        case_ref = self.kwargs['case_id']
        case = resolve_case_by_ref(
            Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO),
            case_ref,
        )
        return case.comentarios.filter(
            estado_moderacion=CaseComment.EstadoModeracion.APROBADO
        ).select_related('usuario')


class CitizenCaseCommentCreateView(APIView):
    """
    MAP-07: POST /api/v1/cases/{case_id}/comments/ (y /api/v1/citizen/cases/{case_id}/comments/)
    Permite comentar un caso publicado; ingresa siempre como `estado_moderacion='pendiente'`.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CaseCommentSerializer

    def post(self, request, case_id):
        case = resolve_case_by_ref(
            Case.objects.filter(estado_publicacion=Case.EstadoPublicacion.APROBADO),
            case_id,
        )
        serializer = CaseCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(
            caso=case,
            usuario=request.user,
            estado_moderacion=CaseComment.EstadoModeracion.PENDIENTE,
        )
        return Response(CaseCommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class AdminCaseCommentModerationViewSet(viewsets.ModelViewSet):
    serializer_class = CaseCommentSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        qs = CaseComment.objects.select_related('caso', 'usuario').all()
        if mod_status := (
            self.request.query_params.get('estado_moderacion')
            or self.request.query_params.get('moderation_status')
        ):
            qs = qs.filter(estado_moderacion__iexact=mod_status)
        if case_id := (self.request.query_params.get('caso') or self.request.query_params.get('case')):
            qs = qs.filter(caso_id=case_id)
        return qs

    def _apply_moderation(self, request):
        comment = self.get_object()
        serializer = CommentModerationActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prev_status = comment.estado_moderacion
        new_status = serializer.validated_data['resolved_status']
        motivo = serializer.validated_data.get('resolved_motivo', '')
        AuditService.set_db_actor_session(request.user)
        comment.estado_moderacion = new_status
        comment.save(update_fields=['estado_moderacion'])

        AuditService.log(
            actor=request.user,
            action='update',
            module='comentarios',
            target_model='comentarios',
            target_id=comment.pk,
            description=f'Moderación de comentario en {comment.caso.codigo}: {prev_status} -> {new_status}',
            previous_data={'estado_moderacion': prev_status},
            new_data={'estado_moderacion': new_status, 'motivo': motivo},
            request=request,
        )

        msg_text = f'Tu comentario fue marcado como {comment.estado_moderacion}.'
        if motivo and serializer.validated_data.get('resolved_notificar_motivo', False):
            msg_text += f' Motivo: {motivo}'
        NotificationService.notify(
            recipient=comment.usuario,
            notification_type='comentario_moderado',
            title=f'Revisión de tu comentario en {comment.caso.codigo}',
            message=msg_text,
            related_case=comment.caso,
        )
        return Response(CaseCommentSerializer(comment).data)

    @extend_schema(
        request=CommentModerationActionSerializer,
        responses={200: CaseCommentSerializer},
        summary='Aprobar, rechazar u ocultar un comentario y guardar motivo en auditoría',
    )
    @action(detail=True, methods=['post'], url_path='moderation')
    def moderation(self, request, pk=None):
        """Sección 14: POST /api/v1/admin/comments/{id}/moderation/"""
        return self._apply_moderation(request)

    @extend_schema(
        request=CommentModerationActionSerializer,
        responses={200: CaseCommentSerializer},
        summary='Alias compatible para moderar un comentario',
    )
    @action(detail=True, methods=['post'], url_path='moderate')
    def moderate(self, request, pk=None):
        """Alias compatible con POST /api/v1/admin/comments/{id}/moderate/"""
        return self._apply_moderation(request)


class PublicEventProposalCreateView(generics.CreateAPIView):
    """PUB-08: POST /api/v1/public/initiative-proposals/ (y /api/v1/citizen/proposals/)"""
    serializer_class = EventProposalSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        usuario = self.request.user if self.request.user.is_authenticated else None
        proposal = serializer.save(usuario=usuario, estado=EventProposal.Estado.PENDIENTE)
        LegalAcceptance.record(
            finalidad='propuesta_iniciativa',
            tipo_documento='tratamiento_datos',
            usuario=usuario,
            propuesta=proposal,
        )


class AdminEventProposalViewSet(viewsets.ModelViewSet):
    """Sección 14: GET / PATCH /api/v1/admin/initiative-proposals/"""
    queryset = EventProposal.objects.select_related('comunidad', 'usuario', 'revisor').all()
    serializer_class = AdminEventProposalSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        serializer.save(revisor=self.request.user, fecha_revision=timezone.now())


class PublicSiteInfoView(APIView):
    """
    PUB-01: GET /api/v1/public/site/
    Proyección pública autorizada de `configuracion_plataforma` y documentos legales vigentes (AMP-09).
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={
            200: inline_serializer(
                name='PublicSiteInfoResponse',
                fields={
                    'institucion': drf_serializers.JSONField(),
                    'configuracion': drf_serializers.DictField(),
                    'documentos_legales': LegalDocumentSerializer(many=True),
                },
            )
        },
        summary='Información institucional pública y políticas vigentes (PUB-01)',
    )
    def get(self, request):
        settings_qs = SiteSetting.objects.filter(clave__in=PUBLIC_SITE_SETTING_KEYS)
        settings_map = {s.clave: s.valor for s in settings_qs}
        LegalDocument.get_current('tratamiento_datos')
        legal_docs = LegalDocument.objects.filter(vigente=True)
        return Response({
            'institucion': settings_map.get(
                'institucion.nombre',
                {'nombre': 'Corporación Pluralismo Social', 'sigla': 'PLUS'},
            ),
            'configuracion': settings_map,
            'documentos_legales': LegalDocumentSerializer(legal_docs, many=True).data,
        })


class NewsletterSubscribeView(APIView):
    """PUB-09 (AMP-02): POST /api/v1/public/newsletter-subscriptions/"""
    permission_classes = [permissions.AllowAny]
    serializer_class = NewsletterSubscriptionSerializer

    def post(self, request):
        serializer = NewsletterSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        correo = serializer.validated_data['resolved_correo']
        nombre = serializer.validated_data.get('nombre') or ''
        user = request.user if request.user.is_authenticated else None

        acceptance = LegalAcceptance.record(
            finalidad='suscripcion_boletin',
            tipo_documento='boletin',
            usuario=user,
            correo_declarado=correo,
        )
        sub, _ = NewsletterSubscription.objects.get_or_create(
            correo=correo,
            defaults={
                'nombre': nombre,
                'usuario': user,
                'estado': NewsletterSubscription.Estado.PENDIENTE,
                'aceptacion_legal': acceptance,
            },
        )
        sub.nombre = nombre or sub.nombre
        sub.usuario = user or sub.usuario
        sub.aceptacion_legal = acceptance
        sub.estado = NewsletterSubscription.Estado.PENDIENTE
        raw_token = sub.generate_token()
        sub.save()

        return Response(
            {
                'id_suscripcion': str(sub.id),
                'correo': sub.correo,
                'estado': sub.estado,
                'confirmation_token': raw_token,
            },
            status=status.HTTP_201_CREATED,
        )


class NewsletterConfirmView(APIView):
    """PUB-10 (AMP-02): POST / GET /api/v1/public/newsletter-subscriptions/confirm/"""
    permission_classes = [permissions.AllowAny]
    serializer_class = NewsletterTokenActionSerializer

    def get(self, request):
        return self.post(request)

    def post(self, request):
        raw_token = (
            request.data.get('token')
            or request.query_params.get('token')
            or ''
        ).strip()
        if not raw_token:
            return Response(
                {'code': 'validation_error', 'message': 'Debe proporcionar el token de confirmación.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token_hash = NewsletterSubscription.hash_token(raw_token)
        sub = NewsletterSubscription.objects.filter(token_hash=token_hash).first()
        if not sub or (sub.expira_en and sub.expira_en < timezone.now()):
            return Response(
                {'code': 'invalid_token', 'message': 'Token de confirmación inválido o expirado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        sub.estado = NewsletterSubscription.Estado.CONFIRMADA
        sub.fecha_confirmacion = timezone.now()
        sub.token_hash = None
        sub.save()

        if sub.usuario_id:
            UserPreference.objects.filter(usuario_id=sub.usuario_id).update(suscrito_boletin=True)

        return Response({'id_suscripcion': str(sub.id), 'estado': sub.estado}, status=status.HTTP_200_OK)


class NewsletterUnsubscribeView(APIView):
    """PUB-11 (AMP-02): POST /api/v1/public/newsletter-subscriptions/unsubscribe/"""
    permission_classes = [permissions.AllowAny]
    serializer_class = NewsletterTokenActionSerializer

    def post(self, request):
        serializer = NewsletterTokenActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw_token = (serializer.validated_data.get('token') or '').strip()
        correo = (
            serializer.validated_data.get('correo')
            or serializer.validated_data.get('email')
            or (request.user.correo if request.user.is_authenticated else '')
        ).strip().lower()

        sub = None
        if raw_token:
            sub = NewsletterSubscription.objects.filter(
                token_hash=NewsletterSubscription.hash_token(raw_token)
            ).first()
        elif correo:
            sub = NewsletterSubscription.objects.filter(correo__iexact=correo).first()

        if sub:
            sub.estado = NewsletterSubscription.Estado.BAJA
            sub.fecha_baja = timezone.now()
            sub.token_hash = None
            sub.save()
            if sub.usuario_id:
                UserPreference.objects.filter(usuario_id=sub.usuario_id).update(suscrito_boletin=False)

        return Response({'estado': 'baja', 'message': 'Suscripción dada de baja exitosamente.'}, status=status.HTTP_200_OK)


class PublicSiteSettingListView(generics.ListAPIView):
    queryset = SiteSetting.objects.filter(clave__in=PUBLIC_SITE_SETTING_KEYS)
    serializer_class = SiteSettingSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class AdminSiteSettingViewSet(viewsets.ModelViewSet):
    queryset = SiteSetting.objects.all()
    serializer_class = SiteSettingSerializer
    permission_classes = [IsAdminOrSuperAdmin]
