from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from apis.serializers.user_serializer import UserSerializer


class CreateUser(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer
