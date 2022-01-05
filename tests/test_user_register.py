import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserRegister(BaseCase):
    def test_user_creation(self):
        data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_contain_key(response, "id")

    def test_user_creation_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists"
