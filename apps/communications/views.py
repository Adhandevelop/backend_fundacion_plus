from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Role, User
from apps.accounts.permissions import IsAdminOrSuperAdmin, IsCitizen
from apps.audit.services import AuditService
from apps.cases.models import Case
from apps.cases.services import CaseService
from apps.communications.models import (
    CaseComment,
    CaseMessage,
    EventProposal,
    SiteSetting,
)
from apps.communications.serializers import (
    AdminEventProposalSerializer,
    CaseCommentSerializer,
    CaseMessageSerializer,
    CommentModerationActionSerializer,
    EventProposalSerializer,
    SiteSettingSerializer,
)
from apps.notifications.services import NotificationService


class CasePrivateMessageListCreateView(APIView):
    """
    GET / POST /api/v1/citizen/cases/{case_id}/messages/ y /api/v1/admin/cases/{case_id}/messages/
    Restringe el acceso estrictamente al ciudadano que reportó el caso, al responsable asignado o al administrador.
    """
    permission_classes = [permissions.IsAuthenticated]

    def _get_authorized_case(self, request, case_id) -> Case:
        case = get_object_or_404(Case, pk=case_id)
        is_reporter = case.usuario_id == request.user.id
        can_manage = CaseService.user_can_manage_case(request.user, case)
        if not (is_reporter or can_manage):
            raise PermissionDenied('No tienes autorización para acceder a los mensajes privados de este caso.')
        return case

    def get(self, request, case_id):
        case = self._get_authorized_case(request, case_id)
        messages_qs = case.mensajes_privados.select_related('remitente', 'destinatario').all()
        messages_qs.filter(destinatario=request.user, fecha_lectura__isnull=True).update(
            fecha_lectura=timezone.now(),
        )
        return Response(CaseMessageSerializer(messages_qs, many=True).data)

    def post(self, request, case_id):
        case = self._get_authorized_case(request, case_id)
        serializer = CaseMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Resolver destinatario si no se envía explícitamente (cumpliendo ck_mensaje_destino: remitente != destinatario)
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


class CitizenCaseCommentCreateView(APIView):
    """
    POST /api/v1/citizen/cases/{case_id}/comments/
    Permite comentar un caso publicado; ingresa siempre como `estado_moderacion='pendiente'`.
    """
    permission_classes = [IsCitizen]

    def post(self, request, case_id):
        case = get_object_or_404(
            Case,
            pk=case_id,
            estado_publicacion=Case.EstadoPublicacion.APROBADO,
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

    @action(detail=True, methods=['post'], url_path='moderate')
    def moderate(self, request, pk=None):
        comment = self.get_object()
        serializer = CommentModerationActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prev_status = comment.estado_moderacion
        new_status = serializer.validated_data['resolved_status']
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
            request=request,
        )

        NotificationService.notify(
            recipient=comment.usuario,
            notification_type='comentario_moderado',
            title=f'Revisión de tu comentario en {comment.caso.codigo}',
            message=f'Tu comentario fue marcado como {comment.estado_moderacion}.',
            related_case=comment.caso,
        )
        return Response(CaseCommentSerializer(comment).data)


class PublicEventProposalCreateView(generics.CreateAPIView):
    serializer_class = EventProposalSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        usuario = self.request.user if self.request.user.is_authenticated else None
        serializer.save(usuario=usuario)


class AdminEventProposalViewSet(viewsets.ModelViewSet):
    queryset = EventProposal.objects.select_related('comunidad', 'usuario', 'revisor').all()
    serializer_class = AdminEventProposalSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def perform_update(self, serializer):
        AuditService.set_db_actor_session(self.request.user)
        serializer.save(revisor=self.request.user, fecha_revision=timezone.now())


class PublicSiteSettingListView(generics.ListAPIView):
    queryset = SiteSetting.objects.all()
    serializer_class = SiteSettingSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class AdminSiteSettingViewSet(viewsets.ModelViewSet):
    queryset = SiteSetting.objects.all()
    serializer_class = SiteSettingSerializer
    permission_classes = [IsAdminOrSuperAdmin]
