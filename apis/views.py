from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apis.serializers.user_serializer import UserSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": "request"})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = self.model.objects.get(username=serializer.validated_data['username'])
        token = Token.objects.create(user=user)
        data = UserSerializer(user, context={"request": request}).data
        data = {'id': data['id'], 'username': data['username'], 'token': token.key}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
