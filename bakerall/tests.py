from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"username": "testcase", "email": "bekadown@gmail.com",
                "password1": "some_strong_psw", "password2": "some_strong_psw"}

        response = self.client.post("/accounts/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND or status.HTTP_201_CREATED)

class AuthenticationTestCase(APITestCase):
    def test_authentication(self):
        data = {"username": "testcase",
                "password": "some_strong_psw"}
        response = self.client.post("/accounts/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LogoutTestCase(APITestCase):
    def test_logout(self):
        response = self.client.post("/accounts/logout/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

class CommentAPIViewTestCase(APITestCase):
    def test_comment(self):
        data = {"author": "admin",
                "comment_text": "text for comment!!!",
                "food": 1}
        response = self.client.post("/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class FoodTestCase(APITestCase):
    def test_food(self):
        data = {
            "name": "food",
            "image": "/img/baker.png",
            "composition": "this is baker",
            "description": "this is baker",
            "pub_date": "07.06.2020",
            "draft": False
        }
        response = self.client.post("/admin/bakerall/food/add/", data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

class GmailAPIViewTestCase(APITestCase):
    def test_gmail(self):
        data = {"name": "levasik",
                "gmail": "lev201611@gmail.com",
                "message": "message text"}
        response = self.client.post("/email/", data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
