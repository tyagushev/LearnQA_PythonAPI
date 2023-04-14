import requests
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
parsed_response = response.json()
token = parsed_response["token"]
seconds = parsed_response["seconds"]
print(f"Task created with token: {token}, will be ready in {seconds} seconds")

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
parsed_response = response.json()
status = parsed_response["status"]
print(f"Status before task is ready: {status}")

time.sleep(seconds)

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
parsed_response = response.json()
status = parsed_response["status"]
if status == "Job is ready":
    result = parsed_response["result"]
    print(f"Task is ready with result: {result}")
else:
    print(f"Error: {parsed_response['error']}")
