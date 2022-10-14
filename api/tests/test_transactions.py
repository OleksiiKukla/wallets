from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)

from transactions.models import Wallet, Transaction


class TransactionsTestCase(APITestCase):
    def setUp(self) -> None:
        url = "/registration/auth/users/"
        data_user1 = {
            "email": "test1@gmail.com",
            "username": "test1",
            "password": "Test1234123",
        }
        data_user2 = {
            "email": "test2@gmail.com",
            "username": "test2",
            "password": "Test1234123",
        }
        data_user3 = {
            "email": "test3@gmail.com",
            "username": "test3",
            "password": "Test1234123",
        }
        data_user4 = {
            "email": "test4@gmail.com",
            "username": "test4",
            "password": "Test1234123",
        }
        self.client.post(url, data_user1, format="json")
        self.client.post(url, data_user2, format="json")
        self.client.post(url, data_user3, format="json")
        self.client.post(url, data_user4, format="json")

        data_wallets = {"type": "visa", "currency": "RUB"}
        self.client.login(username="test1", password="Test1234123")
        self.client.post('/wallets/',data_wallets , format="json")
        self.client.logout()

        self.client.login(username="test2", password="Test1234123")
        self.client.post('/wallets/', data_wallets, format="json")
        self.client.logout()

        data_wallets = {"type": "visa", "currency": "EUR"}
        self.client.login(username="test3", password="Test1234123")
        self.client.post('/wallets/', data_wallets, format="json")
        self.client.logout()

        self.client.login(username="test4", password="Test1234123")
        self.client.post('/wallets/', data_wallets, format="json")
        self.client.logout()


        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)
        self.user3 = User.objects.get(id=3)
        self.user4 = User.objects.get(id=4)
        self.wallet1_user1 = Wallet.objects.get(user= self.user1.id)
        self.wallet1_user2 = Wallet.objects.get(user= self.user2.id)
        self.wallet1_user3 = Wallet.objects.get(user= self.user3.id)
        self.wallet1_user4 = Wallet.objects.get(user= self.user4.id)

    def test_create_new_transaction(self):
        self.client.login(username="test1", password="Test1234123")
        url = "/wallets/transactions/"
        data = {
            "sender": f"{self.wallet1_user1}",
            "receiver": f"{self.wallet1_user2}",
            "transfer_amount": "99.00",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_all_transactions_current_user(self):
        self.client.login(username="test1", password="Test1234123")
        url = '/wallets/transactions/'
        data = {
            "sender": f"{self.wallet1_user1}",
            "receiver": f"{self.wallet1_user2}",
            "transfer_amount": "99.00",
        }
        self.client.post(url, data, format="json")
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    def test_create_transactions_with_difference_currency(self):
        self.client.login(username="test1", password="Test1234123")
        url = '/wallets/transactions/'
        data = {
            "sender": f"{self.wallet1_user1}",
            "receiver": f"{self.wallet1_user3}",
            "transfer_amount": "99.00",
        }
        self.client.post(url, data, format="json")
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

    def test_get_transaction_by_id(self):
        self.client.login(username="test1", password="Test1234123")
        data = {
            "sender": f"{self.wallet1_user1}",
            "receiver": f"{self.wallet1_user2}",
            "transfer_amount": "1.00",
        }
        self.client.post("/wallets/transactions/", data, format="json")
        response = self.client.get('/wallets/transactions/')
        transaction_id = response.data[0]['id']
        url = f'/wallets/transactions/{transaction_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_transactions_wallet_was_sender_or_receiver(self):
        self.client.login(username="test1", password="Test1234123")
        data = {
            "sender": f"{self.wallet1_user1}",
            "receiver": f"{self.wallet1_user2}",
            "transfer_amount": "1.00",
        }
        self.client.post("/wallets/transactions/", data, format="json")
        self.client.logout()

        self.client.login(username="test3", password="Test1234123")
        data = {
            "sender": f"{self.wallet1_user3}",
            "receiver": f"{self.wallet1_user4}",
            "transfer_amount": "1.00",
        }
        self.client.post("/wallets/transactions/", data, format="json")
        response = self.client.get('/wallets/transactions/')
        self.assertEqual(len(response.data), 1)
