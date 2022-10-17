from rest_framework import status
from rest_framework.test import APITestCase


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
