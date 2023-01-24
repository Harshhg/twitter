# Third Party Stuff
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from twitter.users.serializers import AuthUserSerializer, RegisterSerializer, LoginSerializer, EmailVerificationSerializer
from twitter.users.services import create_user_account, get_and_authenticate_user, verify_email


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.pop("email", None)
        user = get_and_authenticate_user(email=email, **serializer.validated_data)
        response_serializer = AuthUserSerializer(
            user, context=self.get_serializer_context()
        )
        return Response(response_serializer.data)

    @action(methods=["POST"], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data)

    @action(methods=["POST"], detail=False)
    def verify_email(self, request, *args, **kwargs):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.pop("email")
        token = serializer.validated_data.pop("token")
        if not verify_email(email, token):
            return Response({"error": "Invalid email / token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": True})
