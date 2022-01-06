import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    missing_parts = [
        "password",
        "username",
        "firstName",
        "lastName",
        "email"
    ]
    names = [
        "a",
        "QdGCpLjmKXUhYseeFkblNpUUrYEeIRWTMraEVVAOirKrZIIvtgIYfxUjsRWUivkvZmEZIWEKWHIwWXhuEazYsAngWhjfLFtJBNxnYGAwWNaos"
        "GaLMiXAIIlSvsiaAqbeEbwNefCpskVWoYQwJRDFMqEylDnStiAzUidDMAUYKcBvvgharRngHJdszQVNYxyRfnzHPVdmbTqENvNrdnkHneSk"
        "CeUFfJeBWoIBxDTBsIgPnhksRHfPrzzzibjrAqIx "
    ]

    def test_user_creation(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_contain_key(response, "id")

    def test_user_creation_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists"

    def test_user_creation_invalid_email(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    @pytest.mark.parametrize("missing_part", missing_parts)
    def test_user_creation_missing_credentials(self, missing_part):
        data = self.prepare_registration_data()
        del data[missing_part]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_part}"

    @pytest.mark.parametrize("name", names)
    def test_user_creation_long_or_short_name(self, name):
        data = self.prepare_registration_data()
        data['firstName'] = name

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        if len(name) > 250:
            assert response.content.decode("utf-8") == "The value of 'firstName' field is too long"
        else:
            assert response.content.decode("utf-8") == "The value of 'firstName' field is too short"
