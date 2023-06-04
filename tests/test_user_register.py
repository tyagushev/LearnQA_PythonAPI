import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.feature("User Registration")
class TestUserRegister(BaseCase):

    @allure.story("Create user successfully")
    def test_crate_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.story("Create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.story("Create user without '@' in email")
    def test_create_user_without_at_in_email(self):
        email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Users response content '{response.content}'"

    @allure.story("Create user without one parameter")
    @pytest.mark.parametrize('username', ['username'])
    def test_create_user_without_one_param(self, username):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        del data[username]

        response = MyRequests.post("/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"The following required params are missed: {username}", \
            f"Unexpected response content '{response.content}'"

    @allure.story("Create user with short name")
    def test_create_user_with_short_name(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'g',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"Unexpected response content '{response.content.decode('utf-8')}'"

    @allure.story("Create user with long name")
    def test_create_user_with_long_name(self):
        email = 'vinkotov@example.com'
        long_name = 'a' * 251  # Генерируем строку с длиной более 250 символов
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': long_name,
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", \
            f"Unexpected response content '{response.content}'"
