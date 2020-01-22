from django.contrib.auth import get_user_model, authenticate, logout, login
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.auth_user import IsUser
from apps.core.get_weather_data import GetWeatherData
from apps.weather_ui.serializers.user_ui_serializer import UserUiRegisterSerializer, UserUiLoginSerializer


class Register(APIView):
    exclude_from_schema = True
    permission_classes = [
        permissions.AllowAny
    ]

    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserUiRegisterSerializer
    template_name = 'auth_or_register.html'

    def get(self, request):
        return Response({'form': self.serializer_class, 'type': 'register'})

    def post(self, request):
        form = self.serializer_class(data=request.data)
        if not form.is_valid():
            return Response({'form': form, 'type': 'register'})
        form.save()
        return redirect('weather:login')


class Login(APIView):
    exclude_from_schema = True
    permission_classes = [
        permissions.AllowAny
    ]
    model = get_user_model()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserUiLoginSerializer
    template_name = 'auth_or_register.html'

    def get(self, request):
        return Response({'form': self.serializer_class, 'type': 'login'})

    def post(self, request):
        form = self.serializer_class(data=request.data)
        if form.is_valid():
            user = authenticate(username=form.validated_data['username'], password=form.validated_data['password'])
            if user is None:
                logout(request)
                return Response({'form': form, 'type': 'login', 'error': True})
            else:
                login(request, user)


        else:
            return Response({'form': form, 'type': 'login'})

        return redirect('weather:weather-ui')


class Logout(IsUser, APIView):
    exclude_from_schema = True

    def get(self, request):
        logout(request)

        return redirect('weather:login')


class Weather(IsUser, APIView):
    template_name = 'weather.html'
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response({'type': 'weather-get'})

    def post(self, request, **kwargs):
        city = request.data['city']

        response = GetWeatherData(city)

        return Response(response)
