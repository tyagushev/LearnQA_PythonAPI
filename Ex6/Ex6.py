import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

redirects = 0
for request in response.history:
    if request.status_code == 301:
        redirects += 1
print(f"Сколько редиректов: {redirects}")
last_url = response.url
print(f"Итоговый url: {last_url}")