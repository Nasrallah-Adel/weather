from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from apps.apis.views import Weather

UserModel = get_user_model()


class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = UserModel.objects.create_user('nasrallah', '12345678')

        self.create_url = reverse('apis:register')

        self.token = Token.objects.create(user=self.test_user)

    def test_create_user(self):
        data = {
            'username': 'nihal',

            'password': '123456789'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(UserModel.objects.count(), 2)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['username'], data['username'])

        self.assertFalse('password' in response.data)

    def test_duplicate_user(self):
        data = {
            'username': 'nasrallah',

            'password': '123456789'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_password(self):
        data = {
            'username': 'nona',

            'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_user_token_exist(self):
        data = {
            'username': 'bebo',

            'password': '123456789'
        }

        response = self.client.post(self.create_url, data, format='json')
        user = UserModel.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)


class WeatherTest(APITestCase):
    def setUp(self):
        self.test_user = UserModel.objects.create_user('nasrallah', '12345678')

        self.create_url = reverse('apis:register')

        self.token = Token.objects.create(user=self.test_user)
        self.view = Weather.as_view()
        self.client.credentials(HTTP_AUTHORIZATION='TOKEN {}'.format(self.token))

    def get_weather_url(self, city):
        weather_url = reverse('apis:weather', kwargs={'city': city})
        return weather_url

    def test_weather_data_true(self):
        response = self.client.get(path=self.get_weather_url("cairo"), )

        self.assertTrue('error_type' not in response.data)
        self.assertTrue('error_info' not in response.data)
        self.assertTrue('location_name' in response.data)
        self.assertTrue('location_country' in response.data)
        self.assertTrue('location_region' in response.data)
        self.assertTrue('location_timezone' in response.data)
        self.assertTrue('location_temperature' in response.data)
        self.assertTrue('location_weather_icons' in response.data)
        self.assertTrue('location_weather_descriptions' in response.data)

    def test_weather_data_false(self):
        response = self.client.get(path=self.get_weather_url("xasx"), )

        self.assertTrue('error_type' in response.data)
        self.assertTrue('error_info' in response.data)
        self.assertTrue('location_name' not in response.data)
        self.assertTrue('location_country' not in response.data)
        self.assertTrue('location_region' not in response.data)
        self.assertTrue('location_timezone' not in response.data)
        self.assertTrue('location_temperature' not in response.data)
        self.assertTrue('location_weather_icons' not in response.data)
        self.assertTrue('location_weather_descriptions' not in response.data)
