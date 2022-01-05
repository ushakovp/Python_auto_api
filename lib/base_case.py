import json.decoder
from requests import Response
from datetime import datetime


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Cannot find header with name {header_name} in the last response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response not in JSON format. Response text is {response.json()}"

        assert name in response_json, f"Response JSON doesn't have key '{name}'"

        return response_json[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            constant_part = "apitest"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{constant_part}{random_part}@{domain}"
        return {
            "password": "1234",
            "username": "apitest",
            "firstName": "apitest",
            "lastName": "apitest",
            "email": email
        }
