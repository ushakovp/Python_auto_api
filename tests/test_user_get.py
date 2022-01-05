import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")
        Assertions.assert_json_contain_key(response, "username")
        Assertions.assert_json_contain_no_keys(response, ["email", "firstName", "lastName", "password"])

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        user_cookie = self.get_cookie(response, "auth_sid")
        cookie = {'auth_sid': user_cookie}
        token = {'x-csrf-token': self.get_header(response, "x-csrf-token")}
        response2 = requests.get("https://playground.learnqa.ru/api/user/2", cookies=cookie, headers=token)
        Assertions.assert_json_contain_keys(response2, ["username", "email", "firstName", "lastName"])
        Assertions.assert_json_contain_no_key(response2, "password")