import requests
import allure
from lib.logger import Logger
from environment import ENV_OBJECT


class MyRequests:
    @staticmethod
    def post(url: str, data: dict = None, cookies: dict = None, headers: dict = None):
        with allure.step(f"POST request to URL '{url}'"):
            return MyRequests._send(url, data, cookies, headers, "POST")

    @staticmethod
    def get(url: str, data: dict = None, cookies: dict = None, headers: dict = None):
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests._send(url, data, cookies, headers, "GET")

    @staticmethod
    def put(url: str, data: dict = None, cookies: dict = None, headers: dict = None):
        with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests._send(url, data, cookies, headers, "PUT")

    @staticmethod
    def delete(url: str, data: dict = None, cookies: dict = None, headers: dict = None):
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests._send(url, data, cookies, headers, "DELETE")

    @staticmethod
    def _send(url: str, data: dict, cookies: dict, headers: dict, method: str):

        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if cookies is None:
            cookies = {}
        if headers is None:
            headers = {}

        Logger.add_request(url, data, cookies, headers, method)

        if method == "GET":
            response = requests.get(url, params=data, cookies=cookies, headers=headers)
        elif method == "POST":
            response = requests.post(url, data=data, cookies=cookies, headers=headers)
        elif method == "PUT":
            response = requests.put(url, params=data, cookies=cookies, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, params=data, cookies=cookies, headers=headers)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(response)

        return response
