import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserRegister(BaseCase):
    def setup(self):
        constant_part = "apitest"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{constant_part}{random_part}@{domain}"

    def test_user_creation(self):
        data = {
            "password": "1234",
            "username": "apitest",
            "firstName": "apitest",
            "lastName": "apitest",
            "email": self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_contain_key(response, "id")

    def test_user_creation_with_existing_email(self):
        email = "vinkotov@example.com"
        data = {
            "password": "1234",
            "username": "apitest",
            "firstName": "apitest",
            "lastName": "apitest",
            "email": email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists"
