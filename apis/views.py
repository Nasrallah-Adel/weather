import requests
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from apis.serializers.user_serializer import UserSerializer

from weather.settings import WEATHER_API_BASE_URL, WEATHER_API_ACCESS_KEY


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


def get_weather_data(weather):
    params = {'access_key': WEATHER_API_ACCESS_KEY,
              'query': weather}
    response = requests.get(url=WEATHER_API_BASE_URL,
                            params=params)

    if response.status_code == status.HTTP_200_OK:

        weather_data = response.json()
        if weather_data.get('error') is not None:
            return {
                "error_type": weather_data['error']['type'],
                'error_info': weather_data['error']['info']
            }
        return {
            'location_name': weather_data['location']['name'],
            'location_country': weather_data['location']['country'],
            'location_region': weather_data['location']['region'],
            'location_timezone': weather_data['location']['timezone_id'],
            'location_temperature': weather_data['current']['temperature'],
            'location_weather_icons': weather_data['current']['weather_icons'],
            'location_weather_descriptions': weather_data['current']['weather_descriptions'],
        }


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

        response = get_weather_data(city)
        status_value = status.HTTP_200_OK

        if response is None:
            status_value = status.HTTP_204_NO_CONTENT

        return Response(response, status=status_value)
