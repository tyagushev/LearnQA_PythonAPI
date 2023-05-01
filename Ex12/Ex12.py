import requests

class TestHeader:
    def test_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        headers = response.headers
        print(headers)
        assert 'x-secret-homework-header' in headers, "В ответе нет заголовка x-secret-homework-header"
        assert response.headers.get('x-secret-homework-header') == 'Some secret value', \
            "В ответе не совпадает значение заголовка Some secret value"