import requests

class TestHomeCookie:

    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookies = dict(response.cookies)
        print(cookies)
        assert 'HomeWork' in cookies, "В ответе нет HomeWork"
        assert cookies.get("HomeWork") == 'hw_value', "В ответе не совпадает значени куки hw_value"