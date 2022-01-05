import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_contain_key(response1, "id")
        email = data['email']
        firstName = data['firstName']
        lastName = data['lastName']
        username = data['username']
        password = data['password']
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        cookie = {'auth_sid': self.get_cookie(response2, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response2, "x-csrf-token")}
        new_name = "newapitest"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 cookies=cookie, headers=token, data={'firstName': new_name})
        Assertions.assert_code_status(response3, 200)

        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}", cookies=cookie, headers=token)

        Assertions.assert_json_contain_keys(response4, ["username", "email", "firstName", "lastName"])
        Assertions.assert_json_contain_no_key(response4, "password")
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Name doesn't change")
