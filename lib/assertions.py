import json
from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_json, f"Response JSON doesn't have key '{name}'"
        assert response_json[name] == expected_value, error_message

    @staticmethod
    def assert_json_contain_key(response: Response, name):
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_json, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_contain_keys(response: Response, names: list):
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_json, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_contain_no_key(response: Response, name):
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name not in response_json, f"Response JSON have key '{name}'"

    @staticmethod
    def assert_json_contain_no_keys(response: Response, names: list):
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        for name in names:
            assert name not in response_json, f"Response JSON have key '{name}'"

    @staticmethod
    def assert_code_status(response: Response, status):
        assert response.status_code == status, f"Unexpected status code {response.status_code}"
