from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    force_authenticate,
    APITestCase,
    APIRequestFactory,
    APIClient,
    RequestsClient,
)

# Create your tests here.
from api.views import WalletListCreate


class WalletApiTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # If the user must be a superuser use User.objects.create_superuser instead of create_user
        self.user = User.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@gmail.com",
            password="Test1234",
        )
        self.client.force_authenticate(self.user)
        # TODO: register user using api http://127.0.0.1:8000/wallets/registration/auth/users/

    def test_create_wallet(self):
        url = "/wallets/"
        data = {"type": "visa", "currency": "RUB"}
        response = self.client.post(url, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_wallets(self):
        url = "http://127.0.0.1:8000/wallets/"
        request = self.factory.get(
            path="http://127.0.0.1:8000/wallets/"
        )  # You can obtain the request in another way
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual()

    def test_get_wallet_by_name(self):
        pass

    def test_delete_wallet(self):
        pass
