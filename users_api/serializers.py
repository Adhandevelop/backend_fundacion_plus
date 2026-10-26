from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs.get('username'),
            **{'password': attrs.get('password')},
        )
        if not user:
            raise serializers.ValidationError('Credenciales inválidas.')
        attrs['user'] = user
        return attrs
