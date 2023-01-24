from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "full_name"]


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "password",
            "email",
            "username",
        ]


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    token = serializers.CharField(max_length=120, required=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name", "username", "email", "auth_token"]

    def get_auth_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key
