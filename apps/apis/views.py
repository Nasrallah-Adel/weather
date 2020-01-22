import requests
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.apis.serializers.user_serializer import UserSerializer
from apps.core.auth_user import IsUser
from apps.core.get_weather_data import GetWeatherData

from weather.settings import WEATHER_API_BASE_URL, WEATHER_API_ACCESS_KEY


class CreateUser(CreateAPIView):
    """
    Register a *User*  by 'username' and 'password'
    ---

    """
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class Weather(IsUser, APIView):

    def get(self, request, **kwargs):
        city = kwargs['city']

        response = GetWeatherData(city)
        status_value = status.HTTP_200_OK

        if response is None:
            status_value = status.HTTP_204_NO_CONTENT

        return Response(response, status=status_value)
