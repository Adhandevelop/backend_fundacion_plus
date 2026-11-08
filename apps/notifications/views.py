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
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.filter(usuario=self.request.user).select_related('caso')
        if leida := (self.request.query_params.get('leida') or self.request.query_params.get('is_read')):
            qs = qs.filter(leida=leida.lower() == 'true')
        return qs

    @action(detail=True, methods=['patch', 'post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        return Response(NotificationSerializer(notification).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        updated = Notification.objects.filter(usuario=request.user, leida=False).update(leida=True)
        return Response({'marked_read_count': updated}, status=status.HTTP_200_OK)
