from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

UserModel = get_user_model()


class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.test_user = UserModel.objects.create_user('nasrallah', '12345678')

        # URL for creating an account.
        self.create_url = reverse('api:register')

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

    def test_create_user_with_short_password(self):

        data = {
            'username': 'ashraf',

            'password': '123'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

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
