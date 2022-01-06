from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_contain_key(response1, "id")
        email = data['email']
        password = data['password']
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        cookie = {'auth_sid': self.get_cookie(response2, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response2, "x-csrf-token")}
        new_name = "newapitest"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   cookies=cookie,
                                   headers=token,
                                   data={'firstName': new_name}
                                   )

        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(f"/user/{user_id}",
                                   cookies=cookie,
                                   headers=token
                                   )

        Assertions.assert_json_contain_keys(response4, ["username", "email", "firstName", "lastName"])
        Assertions.assert_json_contain_no_key(response4, "password")
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Name doesn't change")

    def test_should_not_edit_without_auth(self):
        data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_contain_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        new_name = "newapitest"

        response2 = MyRequests.put(f"/user/{user_id}", data={'firstName': new_name})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Auth token not supplied"

        email = data['email']
        first_name = data['firstName']
        password = data['password']

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        cookie = {'auth_sid': self.get_cookie(response2, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response2, "x-csrf-token")}

        response3 = MyRequests.get(f"/user/{user_id}",
                                   cookies=cookie,
                                   headers=token
                                   )

        Assertions.assert_json_contain_keys(response3, ["username", "email", "firstName", "lastName"])
        Assertions.assert_json_contain_no_key(response3, "password")
        Assertions.assert_json_value_by_name(response3, "firstName", first_name, "Name doesn't change")

    def test_should_not_edit_another_user(self):
        # Create user1
        data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_contain_key(response1, "id")
        email = data['email']
        password = data['password']

        login_data = {
            'email': email,
            'password': password
        }

        # Create user2
        data = self.prepare_registration_data()
        data['firstName'] = "randomName"
        response2 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_contain_key(response1, "id")

        user2_id = self.get_json_value(response2, "id")
        email2 = data['email']
        first_name2 = data['firstName']
        password2 = data['password']

        login_data2 = {
            'email': email2,
            'password': password2
        }

        # Auth user1
        response3 = MyRequests.post("/user/login", data=login_data)

        cookie = {'auth_sid': self.get_cookie(response3, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response3, "x-csrf-token")}
        new_name = "newapitest"

        # Change user2
        response4 = MyRequests.put(f"/user/{user2_id}",
                                   cookies=cookie,
                                   headers=token,
                                   data={'firstName': new_name}
                                   )

        Assertions.assert_code_status(response4, 200)

        # Auth user2
        response5 = MyRequests.post("/user/login", data=login_data2)

        cookie = {'auth_sid': self.get_cookie(response5, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response5, "x-csrf-token")}

        # Check user2
        response6 = MyRequests.get(f"/user/{user2_id}",
                                   cookies=cookie,
                                   headers=token
                                   )

        Assertions.assert_json_contain_keys(response6, ["username", "email", "firstName", "lastName"])
        Assertions.assert_json_contain_no_key(response6, "password")
        Assertions.assert_json_value_by_name(response6, "firstName", first_name2, "Name doesn't change")

    def test_should_not_change_bad_email(self):
        data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_contain_key(response1, "id")
        email = data['email']
        password = data['password']
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        cookie = {'auth_sid': self.get_cookie(response2, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response2, "x-csrf-token")}
        new_mail = "newapitest"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   cookies=cookie,
                                   headers=token,
                                   data={'email': new_mail}
                                   )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Invalid email format"

        response4 = MyRequests.get(f"/user/{user_id}",
                                   cookies=cookie,
                                   headers=token
                                   )

        Assertions.assert_json_contain_keys(response4, ["username", "email", "firstName", "lastName"])
        Assertions.assert_json_contain_no_key(response4, "password")
        Assertions.assert_json_value_by_name(response4, "email", email, "Name doesn't change")

    def test_should_not_change_bad_firstname(self):
        data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_contain_key(response1, "id")
        email = data['email']
        password = data['password']
        first_name = data['firstName']
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        cookie = {'auth_sid': self.get_cookie(response2, "auth_sid")}
        token = {'x-csrf-token': self.get_header(response2, "x-csrf-token")}
        new_name = "s"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   cookies=cookie,
                                   headers=token,
                                   data={'firstName': new_name}
                                   )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3,
                                             "error",
                                             "Too short value for field firstName",
                                             "No or incorrect error message"
                                             )

        response4 = MyRequests.get(f"/user/{user_id}",
                                   cookies=cookie,
                                   headers=token
                                   )

        Assertions.assert_json_contain_keys(response4, ["username", "email", "firstName", "lastName"])
        Assertions.assert_json_contain_no_key(response4, "password")
        Assertions.assert_json_value_by_name(response4, "firstName", first_name, "Name doesn't change")
