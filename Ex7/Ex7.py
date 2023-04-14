import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# Задача 1
response = requests.get(url)
print("Задача 1. Вывод ответа при запросе без параметра method:")
print(response.text)

# Задача 2
response = requests.request("HEAD", url, data={"method": "HEAD"})
print("\nЗадача 2. Вывод ответа при запросе с неизвестным методом:")
print(response.status_code, response.reason)

# Задача 3
methods = ["POST", "GET", "PUT", "DELETE"]
for method in methods:
    payload = {"method": method}
    if method == "GET":
        response = requests.get(url, params=payload)
    else:
        response = requests.post(url, data=payload)
    print(f"\nЗадача 3. Вывод ответа для метода {method}:")
    print(response.text)

# Задача 4
for method in methods:
    for payload_method in methods:
        if method == "GET":
            payload = {"method": payload_method}
            response = requests.get(url, params=payload)
        else:
            payload = {"method": method}
            response = requests.request(payload_method, url, data=payload)
        print(f"\nЗадача 4. Запрос {method} с параметром method={payload_method}:")
        print(response.text)