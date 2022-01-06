from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_service_user(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response = MyRequests.post("/user/login", data=login_data)

        cookie = {'auth_sid': self.get_cookie(response, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response, "x-csrf-token")}

        response = MyRequests.delete(f"/user/2", cookies=cookie, headers=token)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5."

    def test_delete_user_without_auth(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)
        user_id = self.get_json_value(response, "id")

        response = MyRequests.delete(f"/user/{user_id}")

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied"

    def test_delete_user(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        user_id = self.get_json_value(response, "id")
        login_data = {
            'email': data['email'],
            'password': data['password']
        }

        response = MyRequests.post("/user/login", data=login_data)

        cookie = {'auth_sid': self.get_cookie(response, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response, "x-csrf-token")}

        response = MyRequests.delete(f"/user/{user_id}",
                                     cookies=cookie,
                                     headers=token
                                     )

        Assertions.assert_code_status(response, 200)

        response = MyRequests.get(f"/user/{user_id}",
                                  cookies=cookie,
                                  headers=token
                                  )

        Assertions.assert_code_status(response, 404)
        assert response.content.decode("utf-8") == "User not found"

    def test_delete_user_auth_as_another_user(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        user_id = self.get_json_value(response, "id")
        login_data = {
            'email': data['email'],
            'password': data['password']
        }

        data2 = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data2)
        user2_id = self.get_json_value(response, "id")
        login_data2 = {
            'email': data2['email'],
            'password': data2['password']
        }

        response = MyRequests.post("/user/login", data=login_data)

        cookie = {'auth_sid': self.get_cookie(response, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response, "x-csrf-token")}

        response = MyRequests.delete(f"/user/{user2_id}",
                                     cookies=cookie,
                                     headers=token
                                     )

        Assertions.assert_code_status(response, 200)

        response = MyRequests.post("/user/login", data=login_data2)

        cookie2 = {'auth_sid': self.get_cookie(response, "auth_sid")}
        token2 = {'x-csrf-token': self.get_header(response, "x-csrf-token")}

        response = MyRequests.get(f"/user/{user2_id}", cookies=cookie2, headers=token2)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_contain_keys(response, ["username", "email", "firstName", "lastName"])
        Assertions.assert_json_contain_no_key(response, "password")
