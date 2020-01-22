from django.urls import path

from apps.weather_ui.views import *

app_name = 'weather'

urlpatterns = [

    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', Weather.as_view(), name='weather-ui'),

]
