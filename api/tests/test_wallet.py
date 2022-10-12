from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)

from transactions.models import Wallet


class UserCreateApiTestCase(APITestCase):
    def test_create_user(self):
        url = "/registration/auth/users/"
        data = {
            "email": "test1@gmail.com",
            "username": "test1",
            "password": "Test1234123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        url = "/registration/auth/users/"
        data = {
            "email": "test1@gmail.com",
            "username": "test1",
            "password": "Test1234123",
        }
        self.client.post(url, data, format="json")
        login_response = self.client.login(username="test1", password="Test1234123")
        self.assertEqual(login_response, True)

    def test_logout_user(self):
        url = "/registration/auth/users/"
        data = {
            "email": "test1@gmail.com",
            "username": "test1",
            "password": "Test1234123",
        }
        self.client.post(url, data, format="json")
        login_response = self.client.login(username="test1", password="Test1234123")
        # todo при обращении к /walets/ незалогиненым
        #  TypeError: Cannot cast AnonymousUser to int. Are you trying to use it in place of User?
        logout_response = self.client.logout()


class WalletApiTestCase(APITestCase):
    def setUp(self):
        # If the user must be a superuser use User.objects.create_superuser instead of create_user
        self.user = User.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@gmail.com",
            password="Test1234",
        )
        self.client.login(
            username="test", password="Test1234"
        )  # or self.client.force_authenticate(self.user)

    def test_create_wallet(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_more_than_5_wallets(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        for i in range(5):
            response = self.client.post(url, data, format="json")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wallets(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        response = self.client.post(url, data, format="json")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wallet_by_name(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        self.client.post(url, data, format="json")
        wallet = Wallet.objects.get(user_id=self.user.id)
        url = f"/wallets/{wallet.name}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_wallet(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        self.client.post(url, data, format="json")
        wallet = Wallet.objects.get(user_id=self.user.id)
        url = f"/wallets/{wallet.name}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
