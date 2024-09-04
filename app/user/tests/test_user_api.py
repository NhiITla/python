from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test Name",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(
            res.status_code, status.HTTP_201_CREATED
        )  # Corrected status code
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test Name",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars"""
        payload = {
            "email": "test@example.com",
            "password": "test",
            "name": "test Name",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )  # Corrected method name

        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test generate token for valid credential"""
        user_details = {
            "email": "test@example.com",
            "password": "test",
            "name": "test Name",
        }

        create_user(**user_details)

        payload = {
            "email": "test@example.com",
            "password": "test",
            "name": "test Name",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credential(self):
        """Test returns  error if credential invalid"""
        create_user(email="test@example.com", password="goodpass")
        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        payload = {"email": "test@example.com", "password": ""}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
