from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


class UserNotificationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """NOT-01, NOT-02, NOT-03: /api/v1/me/notifications/ y /api/v1/citizen/notifications/"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.filter(usuario=self.request.user).select_related('caso')
        if leida := (self.request.query_params.get('leida') or self.request.query_params.get('is_read')):
            qs = qs.filter(leida=leida.lower() == 'true')
        return qs

    def partial_update(self, request, *args, **kwargs):
        """NOT-02: PATCH /api/v1/me/notifications/{id}/ — Solo permite actualizar `leida`."""
        notification = self.get_object()
        leida_val = request.data.get('leida')
        if leida_val is None:
            leida_val = request.data.get('is_read', True)
        notification.leida = bool(leida_val)
        notification.save(update_fields=['leida'])
        return Response(NotificationSerializer(notification).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch', 'post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        return Response(NotificationSerializer(notification).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='mark-read')
    def bulk_mark_read(self, request):
        """NOT-03: POST /api/v1/me/notifications/mark-read/"""
        qs = Notification.objects.filter(usuario=request.user, leida=False)
        ids = request.data.get('ids') or request.data.get('notification_ids')
        if isinstance(ids, list) and ids:
            qs = qs.filter(id__in=ids)
        updated = qs.update(leida=True)
        remaining = Notification.objects.filter(usuario=request.user, leida=False).count()
        return Response({'marked_read_count': updated, 'unread_remaining': remaining}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        updated = Notification.objects.filter(usuario=request.user, leida=False).update(leida=True)
        return Response({'marked_read_count': updated, 'unread_remaining': 0}, status=status.HTTP_200_OK)
