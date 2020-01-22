from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view

from apps.apis.views import *

app_name = 'apis'

urlpatterns = [

    path('register/', CreateUser.as_view(), name='register'),
    path('login/', views.ObtainAuthToken.as_view(), name='login'),
    path('weather/<str:city>/', Weather.as_view(), name='weather'),

]

