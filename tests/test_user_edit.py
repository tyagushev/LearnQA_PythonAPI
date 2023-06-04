from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.feature("User Edit")
class TestUserEdit(BaseCase):

    @allure.story("Edit just created user")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

        # Попытаемся изменить данные пользователя, будучи неавторизованными

    @allure.story("Edit user unauthorized")
    def test_edit_user_unauthorized(self):
        user_id = 2  # ID пользователя, данные которого мы попытаемся изменить
        new_name = "Changed Name"

        response = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response.content}"

        # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем

    @allure.story("Edit user authorized other user")
    def test_edit_user_authorized_other_user(self):
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

        # Попытаемся изменить данные пользователя 2, будучи авторизованным пользователем 1
        new_name = "Changed Name"

        response4 = MyRequests.put(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response4, 200)
        assert response4.content.decode("utf-8") == "", \
            f"Unexpected response content {response4.content}"

        # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @

    @allure.story("Edit user email invalid")
    def test_edit_user_email_invalid(self):
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

        # Попытаемся изменить email пользователя на недопустимый email без символа "@"
        new_email = "invalidemail.com"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response3.content}"

        # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ"

    @allure.story("Edit user first name invalid")
    def test_edit_user_first_name_invalid(self):
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

        # Попытаемся изменить firstName пользователя на очень короткое значение в один символ
        new_first_name = "A"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_first_name}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.json()["error"] == "Too short value for field firstName", \
            f"Unexpected response content {response3.content}"





