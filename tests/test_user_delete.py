from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.feature("User Delete")
class TestUserDelete(BaseCase):

    @allure.story("Delete user unauthorized")
    def test_delete_user_unauthorized(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response = MyRequests.delete("/user/2", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response.content}"

    @allure.story("Delete user positive")
    def test_delete_user_positive(self):
        # Создаем пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        # Авторизуемся пользователем
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Удаляем пользователя
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)
        assert response3.content.decode("utf-8") == "", \
            f"Unexpected response content {response3.content}"

        # Пытаемся получить данные удаленного пользователя
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response4.content}"

    @allure.story("Delete user authorized other user")
    def test_delete_user_authorized_other_user(self):
        # Создаем пользователя 1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        user_id1 = self.get_json_value(response1, "id")

        # Создаем пользователя 2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        user_id2 = self.get_json_value(response2, "id")

        # Авторизуемся пользователем 1
        login_data1 = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }
        response3 = MyRequests.post("/user/login", data=login_data1)

        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # Попытаемся удалить пользователя 2, будучи авторизованным пользователем 1
        response4 = MyRequests.delete(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1}
        )

        Assertions.assert_code_status(response4, 200)
