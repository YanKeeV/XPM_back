from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver

import core.scheme

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)


class RegistrationAPIView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    renderer_classes = [UserJSONRenderer]

    def post(self, request):

        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):

    permission_classes = [AllowAny,]
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):

        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated,]
    renderer_classes = [UserJSONRenderer]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class SetImageAPIView(APIView):

    permission_classes = [IsAuthenticated,]
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):

        user = request.user
        print(request.data)
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    send_mail(
        # Title:
        "Password Reset for {title}".format(title="XPManager"),
        # Message:
        # change link for release
        "Use the following link to reset your password: http://localhost:5173/login/resetpassword/confirm?token={token}".format(token=reset_password_token.key),
        # From:
        "your-email@gmail.com",
        # To:
        [reset_password_token.user.email]
    )