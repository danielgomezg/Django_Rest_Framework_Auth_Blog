from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from django.contrib.auth import get_user_model

#Esto siempre se hace en cualquier archivo que no sea models, para obtener el modelo usuario
User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    qr_code = serializers.URLField(source="get_qr_code")
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    #con el source se indica que se usa el metodo creado en el modelo
    qr_code = serializers.URLField(source="get_qr_code")
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "updated_at",
            "two_factor_enabled",
            "otpauth_url",
            "login_otp",
            "login_otp_used",
            "otp_created_at",
            "qr_code",
        ]


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "updated_at",
        ]