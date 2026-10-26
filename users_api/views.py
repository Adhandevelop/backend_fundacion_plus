from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users_api.permissions import IsAdministrativo, IsCliente
from users_api.serializers import LoginSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        role = 'administrativo' if user.is_staff else 'cliente'
        return Response(
            {
                'token': token.key,
                'usuario': user.username,
                'rol': role,
            },
            status=status.HTTP_200_OK,
        )


class ClienteProfileView(APIView):
    permission_classes = [IsCliente]

    def get(self, request):
        return Response(
            {
                'usuario': request.user.username,
                'rol': 'cliente',
            },
            status=status.HTTP_200_OK,
        )


class AdministrativoProfileView(APIView):
    permission_classes = [IsAdministrativo]

    def get(self, request):
        return Response(
            {
                'usuario': request.user.username,
                'rol': 'administrativo',
            },
            status=status.HTTP_200_OK,
        )

# Create your views here.
