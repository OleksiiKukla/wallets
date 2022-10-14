from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)

from transactions.models import Wallet


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
            self.client.post(url, data, format="json")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wallets(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        self.client.post(url, data, format="json")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wallets_without_login(self):
        self.client.logout()
        url = "/wallets/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_wallet_by_name(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        self.client.post(url, data, format="json")
        wallet = Wallet.objects.get(user_id=self.user.id)
        url = f"/wallets/{wallet.name}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wallet_by_name_without_login(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        self.client.post(url, data, format="json")
        self.client.logout()
        wallet = Wallet.objects.get(user_id=self.user.id)
        url = f"/wallets/{wallet.name}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_wallet(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        self.client.post(url, data, format="json")
        wallet = Wallet.objects.get(user_id=self.user.id)
        url = f"/wallets/{wallet.name}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_method_put_wallet(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_method_patch_wallet(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
