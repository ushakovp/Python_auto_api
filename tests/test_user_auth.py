import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookies",
        "no_token"
    ]

    def setup(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response, "auth_sid")
        self.token = self.get_header(response, "x-csrf-token")
        self.user_id_from_login = self.get_json_value(response, "user_id")

    def test_auth_user(self):
        response = MyRequests.get("/user/auth",
                                  headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid}
                                  )

        Assertions.assert_json_value_by_name(
            response,
            "user_id",
            self.user_id_from_login,
            "User id from login method is not equal to user id from auth method"
        )

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth(self, condition):
        if condition == "no_cookie":
            response = MyRequests.get("/user/auth",
                                      headers={'x-csrf-token': self.token},
                                      )
        else:
            response = MyRequests.get("/user/auth",
                                      cookies={'auth_sid': self.auth_sid}
                                      )

        Assertions.assert_json_value_by_name(
            response,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
